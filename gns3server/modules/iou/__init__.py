# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 GNS3 Technologies Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
IOU server module.
"""

import os
import sys
import base64
import tempfile
from gns3server.modules import IModule
from gns3server.config import Config
from .iou_device import IOUDevice
from .iou_error import IOUError
from .nios.nio_udp import NIO_UDP
import gns3server.jsonrpc as jsonrpc

import logging
log = logging.getLogger(__name__)


class IOU(IModule):
    """
    IOU module.

    :param name: module name
    :param args: arguments for the module
    :param kwargs: named arguments for the module
    """

    def __init__(self, name, *args, **kwargs):

        # get the iouyap location
        config = Config.instance()
        iou_config = config.get_section_config(name.upper())
        self._iouyap = iou_config.get("iouyap")
        if not self._iouyap:
            for path in os.environ["PATH"].split(":"):
                if "iouyap" in os.listdir(path) and os.access("iouyap", os.X_OK):
                    self._iouyap = os.path.join(path, "iouyap")
                    break

        if not self._iouyap or not os.path.exists(self._iouyap):
            raise IOUError("iouyap binary couldn't be found!")

        if not os.access(self._iouyap, os.X_OK):
            raise IOUError("iouyap is not executable")

        # a new process start when calling IModule
        IModule.__init__(self, name, *args, **kwargs)
        self._remote_server = False
        self._iou_instances = {}
        self._console_start_port_range = 4001
        self._console_end_port_range = 4512
        self._current_console_port = self._console_start_port_range
        self._udp_start_port_range = 30001
        self._udp_end_port_range = 40001
        self._current_udp_port = self._udp_start_port_range
        self._host = "127.0.0.1"  # FIXME: used by ZeroMQ...
        self._projects_dir = kwargs["projects_dir"]
        self._tempdir = kwargs["temp_dir"]
        self._working_dir = self._projects_dir
        self._iourc = ""

        self._iou_callback = self.add_periodic_callback(self._check_iou, 5000)
        self._iou_callback.start()

    def stop(self):
        """
        Properly stops the module.
        """

        # delete all IOU instances
        for iou_id in self._iou_instances:
            iou_instance = self._iou_instances[iou_id]
            iou_instance.delete()

        IModule.stop(self)  # this will stop the I/O loop

    def _check_iou(self):

        for iou_id in self._iou_instances:
            iou_instance = self._iou_instances[iou_id]
            if iou_instance.started and not iou_instance.is_running():
                self.send_notification({"module": self.name,
                                        "id": iou_id,
                                        "name": iou_instance.name,
                                        "message": "IOU is not running"})
                iou_instance.stop()

    @IModule.route("iou.reset")
    def reset(self, request):
        """
        Resets the module.

        :param request: JSON request
        """

        # delete all IOU instances
        for iou_id in self._iou_instances:
            iou_instance = self._iou_instances[iou_id]
            iou_instance.delete()

        # resets the instance IDs
        IOUDevice.reset()

        self._iou_instances.clear()
        self._remote_server = False
        self._current_console_port = self._console_start_port_range
        self._current_udp_port = self._udp_start_port_range

        if self._iourc and os.path.exists(self._iourc):
            try:
                os.remove(self._iourc)
            except EnvironmentError as e:
                log.warn("could not delete iourc file {}: {}".format(self._iourc, e))

        log.info("IOU module has been reset")

    @IModule.route("iou.settings")
    def settings(self, request):
        """
        Set or update settings.

        Mandatory request parameters:
        - iourc (base64 encoded iourc file)

        Optional request parameters:
        - working_dir (path to a working directory)
        - console_start_port_range
        - console_end_port_range
        - udp_start_port_range
        - udp_end_port_range

        :param request: JSON request
        """

        if request == None:
            self.send_param_error()
            return

        if "iourc" in request:
            base64iourc = base64.decodestring(request["iourc"].encode("utf-8"))
            try:
                with tempfile.NamedTemporaryFile(delete=False) as f:
                    log.info("saving iourc file content to {}".format(f.name))
                    f.write(base64iourc)
                    self._iourc = f.name
            except EnvironmentError as e:
                raise IOUError("Could not save iourc file to {}: {}".format(f.name, e))

        if "working_dir" in request and self._working_dir != request["working_dir"]:
            self._working_dir = request["working_dir"]
            log.info("this server is local with working directory path to {}".format(self._working_dir))
            for iou_id in self._iou_instances:
                iou_instance = self._iou_instances[iou_id]
                iou_instance.working_dir = self._working_dir
        else:
            self._remote_server = True
            log.info("this server is remote")
            self._working_dir = self._projects_dir

        if "console_start_port_range" in request and "console_end_port_range" in request:
            self._console_start_port_range = request["console_start_port_range"]
            self._console_end_port_range = request["console_end_port_range"]

        if "udp_start_port_range" in request and "udp_end_port_range" in request:
            self._udp_start_port_range = request["udp_start_port_range"]
            self._udp_end_port_range = request["udp_end_port_range"]

        log.debug("received request {}".format(request))

    @IModule.route("iou.create")
    def iou_create(self, request):
        """
        Creates a new IOU instance.

        Optional request parameters:
        - name (IOU name)
        - path (path to the IOU executable)

        Response parameters:
        - id (IOU instance identifier)
        - name (IOU name)

        :param request: JSON request
        """

        #TODO: JSON schema validation for the request
        name = None
        if request and "name" in request:
            name = request["name"]

        iou_path = request["path"]

        try:
            iou_instance = IOUDevice(iou_path, self._working_dir, name=name)
            # find a console port
            if self._current_console_port >= self._console_end_port_range:
                self._current_console_port = self._console_start_port_range
            iou_instance.console = IOUDevice.find_unused_port(self._current_console_port, self._console_end_port_range, self._host)
            self._current_console_port += 1
        except IOUError as e:
            self.send_custom_error(str(e))
            return

        response = {"name": iou_instance.name,
                    "id": iou_instance.id}

        defaults = iou_instance.defaults()
        response.update(defaults)
        self._iou_instances[iou_instance.id] = iou_instance
        self.send_response(response)

    @IModule.route("iou.delete")
    def iou_delete(self, request):
        """
        Deletes an IOU instance.

        Mandatory request parameters:
        - id (IOU instance identifier)

        Response parameters:
        - same as original request

        :param request: JSON request
        """

        if request == None:
            self.send_param_error()
            return

        #TODO: JSON schema validation for the request
        log.debug("received request {}".format(request))
        iou_id = request["id"]
        iou_instance = self._iou_instances[iou_id]
        try:
            iou_instance.delete()
            del self._iou_instances[iou_id]
        except IOUError as e:
            self.send_custom_error(str(e))
            return
        self.send_response(request)

    @IModule.route("iou.update")
    def iou_update(self, request):
        """
        Updates an IOU instance

        Mandatory request parameters:
        - id (IOU instance identifier)

        Optional request parameters:
        - any setting to update
        - startup_config_base64 (startup-config base64 encoded)

        Response parameters:
        - same as original request

        :param request: JSON request
        """

        if request == None:
            self.send_param_error()
            return

        #TODO: JSON schema validation for the request
        log.debug("received request {}".format(request))
        iou_id = request["id"]
        iou_instance = self._iou_instances[iou_id]

        try:
            # a new startup-config has been pushed
            if "startup_config_base64" in request:
                config = base64.decodestring(request["startup_config_base64"].encode("utf-8")).decode("utf-8")
                config = "!\n" + config.replace("\r", "")
                config = config.replace('%h', iou_instance.name)
                config_path = os.path.join(iou_instance.working_dir, "startup-config")
                try:
                    with open(config_path, "w") as f:
                        log.info("saving startup-config to {}".format(config_path))
                        f.write(config)
                except EnvironmentError as e:
                    raise IOUError("Could not save the configuration {}: {}".format(config_path, e))
                request["startup_config"] = os.path.basename(config_path)
            if "startup_config" in request:
                iou_instance.startup_config = request["startup_config"]
        except IOUError as e:
            self.send_custom_error(str(e))
            return

        for name, value in request.items():
            if hasattr(iou_instance, name) and getattr(iou_instance, name) != value:
                try:
                    setattr(iou_instance, name, value)
                except IOUError as e:
                    self.send_custom_error(str(e))
                    return

        self.send_response(request)

    @IModule.route("iou.start")
    def vm_start(self, request):
        """
        Starts an IOU instance.

        Mandatory request parameters:
        - id (IOU instance identifier)

        Response parameters:
        - same as original request

        :param request: JSON request
        """

        if request == None:
            self.send_param_error()
            return

        #TODO: JSON schema validation for the request
        log.debug("received request {}".format(request))
        iou_id = request["id"]
        iou_instance = self._iou_instances[iou_id]
        try:
            log.debug("starting IOU with command: {}".format(iou_instance.command()))
            iou_instance.iouyap = self._iouyap
            iou_instance.iourc = self._iourc
            iou_instance.start()
        except IOUError as e:
            self.send_custom_error(str(e))
            return
        self.send_response(request)

    @IModule.route("iou.stop")
    def vm_stop(self, request):
        """
        Stops an IOU instance.

        Mandatory request parameters:
        - id (IOU instance identifier)

        Response parameters:
        - same as original request

        :param request: JSON request
        """

        if request == None:
            self.send_param_error()
            return

        #TODO: JSON schema validation for the request
        log.debug("received request {}".format(request))
        iou_id = request["id"]
        iou_instance = self._iou_instances[iou_id]
        try:
            iou_instance.stop()
        except IOUError as e:
            self.send_custom_error(str(e))
            return
        self.send_response(request)

    @IModule.route("iou.reload")
    def vm_reload(self, request):
        """
        Reloads an IOU instance.

        Mandatory request parameters:
        - id (IOU identifier)

        Response parameters:
        - same as original request

        :param request: JSON request
        """

        if request == None:
            self.send_param_error()
            return

        #TODO: JSON schema validation for the request
        log.debug("received request {}".format(request))
        iou_id = request["id"]
        iou_instance = self._iou_instances[iou_id]
        try:
            if iou_instance.is_running():
                iou_instance.stop()
            iou_instance.start()
        except IOUError as e:
            self.send_custom_error(str(e))
            return
        self.send_response(request)

    @IModule.route("iou.allocate_udp_port")
    def allocate_udp_port(self, request):
        """
        Allocates a UDP port in order to create an UDP NIO.

        Mandatory request parameters:
        - id (IOU identifier)
        - port_id (unique port identifier)

        Response parameters:
        - port_id (unique port identifier)
        - lhost (local host address)
        - lport (allocated local port)

        :param request: JSON request
        """

        if request == None:
            self.send_param_error()
            return

        #TODO: JSON schema validation for the request
        log.debug("received request {}".format(request))
        iou_id = request["id"]
        iou_instance = self._iou_instances[iou_id]

        try:

            # find a UDP port
            if self._current_udp_port >= self._udp_end_port_range:
                self._current_udp_port = self._udp_start_port_range
            port = IOUDevice.find_unused_port(self._current_udp_port, self._udp_end_port_range, host=self._host, socket_type="UDP")
            self._current_udp_port += 1

            log.info("{} [id={}] has allocated UDP port {} with host {}".format(iou_instance .name,
                                                                                iou_instance .id,
                                                                                port,
                                                                                self._host))
            response = {"lport": port,
                        "lhost": self._host}

        except IOUError as e:
            self.send_custom_error(str(e))
            return

        response["port_id"] = request["port_id"]
        self.send_response(response)

    @IModule.route("iou.add_nio")
    def add_nio(self, request):
        """
        Adds an NIO (Network Input/Output) for an IOU instance.

        Mandatory request parameters:
        - id (IOU instance identifier)
        - slot (slot number)
        - port (port number)
        - port_id (unique port identifier)
        - nio (nio type, one of the following)
            - "NIO_UDP"
                - lport (local port)
                - rhost (remote host)
                - rport (remote port)

        Response parameters:
        - same as original request

        :param request: JSON request
        """

        if request == None:
            self.send_param_error()
            return

        #TODO: JSON schema validation for the request
        log.debug("received request {}".format(request))
        iou_id = request["id"]
        iou_instance = self._iou_instances[iou_id]

        slot = request["slot"]
        port = request["port"]

        try:
            nio = None
            #TODO: support for TAP and Ethernet NIOs
            if request["nio"] == "NIO_UDP":
                lport = request["lport"]
                rhost = request["rhost"]
                rport = request["rport"]
                nio = NIO_UDP(lport, rhost, rport)
            if not nio:
                raise IOUError("Requested NIO doesn't exist or is not supported: {}".format(request["nio"]))
        except IOUError as e:
            self.send_custom_error(str(e))
            return

        try:
            iou_instance.slot_add_nio_binding(slot, port, nio)
        except IOUError as e:
            self.send_custom_error(str(e))
            return

        # for now send back the original request
        self.send_response(request)

    @IModule.route("iou.delete_nio")
    def delete_nio(self, request):
        """
        Deletes an NIO (Network Input/Output).

        Mandatory request parameters:
        - id (IOU instance identifier)
        - slot (slot identifier)
        - port (port identifier)

        Response parameters:
        - same as original request

        :param request: JSON request
        """

        if request == None:
            self.send_param_error()
            return

        #TODO: JSON schema validation for the request
        log.debug("received request {}".format(request))
        iou_id = request["id"]
        iou_instance = self._iou_instances[iou_id]
        slot = request["slot"]
        port = request["port"]

        try:
            iou_instance.slot_remove_nio_binding(slot, port)
        except IOUError as e:
            self.send_custom_error(str(e))
            return

        # for now send back the original request
        self.send_response(request)

    @IModule.route("iou.echo")
    def echo(self, request):
        """
        Echo end point for testing purposes.

        :param request: JSON request
        """

        if request == None:
            self.send_param_error()
        else:
            log.debug("received request {}".format(request))
            self.send_response(request)