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


VBOX_CREATE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "Request validation to create a new VirtualBox VM instance",
    "type": "object",
    "properties": {
        "name": {
            "description": "VirtualBox VM instance name",
            "type": "string",
            "minLength": 1,
        },
        "vmname": {
            "description": "VirtualBox VM name (in VirtualBox itself)",
            "type": "string",
            "minLength": 1,
        },
        "vbox_id": {
            "description": "VirtualBox VM instance ID",
            "type": "integer"
        },
        "console": {
            "description": "console TCP port",
            "minimum": 1,
            "maximum": 65535,
            "type": "integer"
        },
    },
    "additionalProperties": False,
    "required": ["name", "vmname"],
}

VBOX_DELETE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "Request validation to delete a VirtualBox VM instance",
    "type": "object",
    "properties": {
        "id": {
            "description": "VirtualBox VM instance ID",
            "type": "integer"
        },
    },
    "additionalProperties": False,
    "required": ["id"]
}

VBOX_UPDATE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "Request validation to update a VirtualBox VM instance",
    "type": "object",
    "properties": {
        "id": {
            "description": "VirtualBox VM instance ID",
            "type": "integer"
        },
        "name": {
            "description": "VirtualBox VM instance name",
            "type": "string",
            "minLength": 1,
        },
        "vmname": {
            "description": "VirtualBox VM name (in VirtualBox itself)",
            "type": "string",
            "minLength": 1,
        },
        "adapters": {
            "description": "number of adapters",
            "type": "integer",
            "minimum": 1,
            "maximum": 36,  # maximum given by the ICH9 chipset in VirtualBox
        },
        "adapter_start_index": {
            "description": "adapter index from which to start using adapters",
            "type": "integer",
            "minimum": 0,
            "maximum": 35,  # maximum given by the ICH9 chipset in VirtualBox
        },
        "adapter_type": {
            "description": "VirtualBox adapter type",
            "type": "string",
            "minLength": 1,
        },
        "console": {
            "description": "console TCP port",
            "minimum": 1,
            "maximum": 65535,
            "type": "integer"
        },
        "enable_console": {
            "description": "enable the console",
            "type": "boolean"
        },
        "headless": {
            "description": "headless mode",
            "type": "boolean"
        },
    },
    "additionalProperties": False,
    "required": ["id"]
}

VBOX_START_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "Request validation to start a VirtualBox VM instance",
    "type": "object",
    "properties": {
        "id": {
            "description": "VirtualBox VM instance ID",
            "type": "integer"
        },
    },
    "additionalProperties": False,
    "required": ["id"]
}

VBOX_STOP_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "Request validation to stop a VirtualBox VM instance",
    "type": "object",
    "properties": {
        "id": {
            "description": "VirtualBox VM instance ID",
            "type": "integer"
        },
    },
    "additionalProperties": False,
    "required": ["id"]
}

VBOX_SUSPEND_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "Request validation to suspend a VirtualBox VM instance",
    "type": "object",
    "properties": {
        "id": {
            "description": "VirtualBox VM instance ID",
            "type": "integer"
        },
    },
    "additionalProperties": False,
    "required": ["id"]
}

VBOX_RELOAD_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "Request validation to reload a VirtualBox VM instance",
    "type": "object",
    "properties": {
        "id": {
            "description": "VirtualBox VM instance ID",
            "type": "integer"
        },
    },
    "additionalProperties": False,
    "required": ["id"]
}

VBOX_ALLOCATE_UDP_PORT_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "Request validation to allocate an UDP port for a VirtualBox VM instance",
    "type": "object",
    "properties": {
        "id": {
            "description": "VirtualBox VM instance ID",
            "type": "integer"
        },
        "port_id": {
            "description": "Unique port identifier for the VirtualBox VM instance",
            "type": "integer"
        },
    },
    "additionalProperties": False,
    "required": ["id", "port_id"]
}

VBOX_ADD_NIO_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "Request validation to add a NIO for a VirtualBox VM instance",
    "type": "object",

    "definitions": {
        "UDP": {
            "description": "UDP Network Input/Output",
            "properties": {
                "type": {
                    "enum": ["nio_udp"]
                },
                "lport": {
                    "description": "Local port",
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 65535
                },
                "rhost": {
                    "description": "Remote host",
                    "type": "string",
                    "minLength": 1
                },
                "rport": {
                    "description": "Remote port",
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 65535
                }
            },
            "required": ["type", "lport", "rhost", "rport"],
            "additionalProperties": False
        },
        "Ethernet": {
            "description": "Generic Ethernet Network Input/Output",
            "properties": {
                "type": {
                    "enum": ["nio_generic_ethernet"]
                },
                "ethernet_device": {
                    "description": "Ethernet device name e.g. eth0",
                    "type": "string",
                    "minLength": 1
                },
            },
            "required": ["type", "ethernet_device"],
            "additionalProperties": False
        },
        "LinuxEthernet": {
            "description": "Linux Ethernet Network Input/Output",
            "properties": {
                "type": {
                    "enum": ["nio_linux_ethernet"]
                },
                "ethernet_device": {
                    "description": "Ethernet device name e.g. eth0",
                    "type": "string",
                    "minLength": 1
                },
            },
            "required": ["type", "ethernet_device"],
            "additionalProperties": False
        },
        "TAP": {
            "description": "TAP Network Input/Output",
            "properties": {
                "type": {
                    "enum": ["nio_tap"]
                },
                "tap_device": {
                    "description": "TAP device name e.g. tap0",
                    "type": "string",
                    "minLength": 1
                },
            },
            "required": ["type", "tap_device"],
            "additionalProperties": False
        },
        "UNIX": {
            "description": "UNIX Network Input/Output",
            "properties": {
                "type": {
                    "enum": ["nio_unix"]
                },
                "local_file": {
                    "description": "path to the UNIX socket file (local)",
                    "type": "string",
                    "minLength": 1
                },
                "remote_file": {
                    "description": "path to the UNIX socket file (remote)",
                    "type": "string",
                    "minLength": 1
                },
            },
            "required": ["type", "local_file", "remote_file"],
            "additionalProperties": False
        },
        "VDE": {
            "description": "VDE Network Input/Output",
            "properties": {
                "type": {
                    "enum": ["nio_vde"]
                },
                "control_file": {
                    "description": "path to the VDE control file",
                    "type": "string",
                    "minLength": 1
                },
                "local_file": {
                    "description": "path to the VDE control file",
                    "type": "string",
                    "minLength": 1
                },
            },
            "required": ["type", "control_file", "local_file"],
            "additionalProperties": False
        },
        "NULL": {
            "description": "NULL Network Input/Output",
            "properties": {
                "type": {
                    "enum": ["nio_null"]
                },
            },
            "required": ["type"],
            "additionalProperties": False
        },
    },

    "properties": {
        "id": {
            "description": "VirtualBox VM instance ID",
            "type": "integer"
        },
        "port_id": {
            "description": "Unique port identifier for the VirtualBox VM instance",
            "type": "integer"
        },
        "port": {
            "description": "Port number",
            "type": "integer",
            "minimum": 0,
            "maximum": 36  # maximum given by the ICH9 chipset in VirtualBox
        },
        "nio": {
            "type": "object",
            "description": "Network Input/Output",
            "oneOf": [
                {"$ref": "#/definitions/UDP"},
                {"$ref": "#/definitions/Ethernet"},
                {"$ref": "#/definitions/LinuxEthernet"},
                {"$ref": "#/definitions/TAP"},
                {"$ref": "#/definitions/UNIX"},
                {"$ref": "#/definitions/VDE"},
                {"$ref": "#/definitions/NULL"},
            ]
        },
    },
    "additionalProperties": False,
    "required": ["id", "port_id", "port", "nio"]
}


VBOX_DELETE_NIO_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "Request validation to delete a NIO for a VirtualBox VM instance",
    "type": "object",
    "properties": {
        "id": {
            "description": "VirtualBox VM instance ID",
            "type": "integer"
        },
        "port": {
            "description": "Port number",
            "type": "integer",
            "minimum": 0,
            "maximum": 36  # maximum given by the ICH9 chipset in VirtualBox
        },
    },
    "additionalProperties": False,
    "required": ["id", "port"]
}

VBOX_START_CAPTURE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "Request validation to start a packet capture on a VirtualBox VM instance port",
    "type": "object",
    "properties": {
        "id": {
            "description": "VirtualBox VM instance ID",
            "type": "integer"
        },
        "port": {
            "description": "Port number",
            "type": "integer",
            "minimum": 0,
            "maximum": 36  # maximum given by the ICH9 chipset in VirtualBox
        },
        "port_id": {
            "description": "Unique port identifier for the VirtualBox VM instance",
            "type": "integer"
        },
        "capture_file_name": {
            "description": "Capture file name",
            "type": "string",
            "minLength": 1,
        },
    },
    "additionalProperties": False,
    "required": ["id", "port", "port_id", "capture_file_name"]
}

VBOX_STOP_CAPTURE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "Request validation to stop a packet capture on a VirtualBox VM instance port",
    "type": "object",
    "properties": {
        "id": {
            "description": "VirtualBox VM instance ID",
            "type": "integer"
        },
        "port": {
            "description": "Port number",
            "type": "integer",
            "minimum": 0,
            "maximum": 36  # maximum given by the ICH9 chipset in VirtualBox
        },
        "port_id": {
            "description": "Unique port identifier for the VirtualBox VM instance",
            "type": "integer"
        },
    },
    "additionalProperties": False,
    "required": ["id", "port", "port_id"]
}

