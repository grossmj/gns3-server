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

VM_CREATE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "Request validation to create a new VM instance",
    "type": "object",
    "properties": {
        "name": {
            "description": "Router name",
            "type": "string",
            "minLength": 1,
        },
        "router_id": {
            "description": "VM/router instance ID",
            "type": "integer"
        },
        "platform": {
            "description": "router platform",
            "type": "string",
            "minLength": 1,
            "pattern": "^c[0-9]{4}$"
        },
        "chassis": {
            "description": "router chassis model",
            "type": "string",
            "minLength": 1,
            "pattern": "^[0-9]{4}(XM)?$"
        },
        "image": {
            "description": "path to the IOS image file",
            "type": "string",
            "minLength": 1
        },
        "ram": {
            "description": "amount of RAM in MB",
            "type": "integer"
        },
        "console": {
            "description": "console TCP port",
            "type": "integer",
            "minimum": 1,
            "maximum": 65535
        },
        "aux": {
            "description": "auxiliary console TCP port",
            "type": "integer",
            "minimum": 1,
            "maximum": 65535
        },
        "mac_addr": {
            "description": "base MAC address",
            "type": "string",
            "minLength": 1,
            "pattern": "^([0-9a-fA-F]{4}\\.){2}[0-9a-fA-F]{4}$"
        }
    },
    "additionalProperties": False,
    "required": ["name", "platform", "image", "ram"]
}

VM_DELETE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "Request validation to delete a VM instance",
    "type": "object",
    "properties": {
        "id": {
            "description": "VM instance ID",
            "type": "integer"
        },
    },
    "additionalProperties": False,
    "required": ["id"]
}

VM_START_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "Request validation to start a VM instance",
    "type": "object",
    "properties": {
        "id": {
            "description": "VM instance ID",
            "type": "integer"
        },
    },
    "additionalProperties": False,
    "required": ["id"]
}

VM_STOP_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "Request validation to stop a VM instance",
    "type": "object",
    "properties": {
        "id": {
            "description": "VM instance ID",
            "type": "integer"
        },
    },
    "additionalProperties": False,
    "required": ["id"]
}

VM_SUSPEND_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "Request validation to suspend a VM instance",
    "type": "object",
    "properties": {
        "id": {
            "description": "VM instance ID",
            "type": "integer"
        },
    },
    "additionalProperties": False,
    "required": ["id"]
}

VM_RELOAD_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "Request validation to reload a VM instance",
    "type": "object",
    "properties": {
        "id": {
            "description": "VM instance ID",
            "type": "integer"
        },
    },
    "additionalProperties": False,
    "required": ["id"]
}

#TODO: improve platform specific properties (dependencies?)
VM_UPDATE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "Request validation to update a VM instance",
    "type": "object",
    "properties": {
        "id": {
            "description": "VM instance ID",
            "type": "integer"
        },
        "name": {
            "description": "Router name",
            "type": "string",
            "minLength": 1,
        },
        "platform": {
            "description": "platform",
            "type": "string",
            "minLength": 1,
            "pattern": "^c[0-9]{4}$"
        },
        "image": {
            "description": "path to the IOS image",
            "type": "string",
            "minLength": 1,
        },
        "startup_config": {
            "description": "path to the IOS startup configuration file",
            "type": "string",
            "minLength": 1,
        },
        "private_config": {
            "description": "path to the IOS private configuration file",
            "type": "string",
            "minLength": 1,
        },
        "ram": {
            "description": "amount of RAM in MB",
            "type": "integer"
        },
        "nvram": {
            "description": "amount of NVRAM in KB",
            "type": "integer"
        },
        "mmap": {
            "description": "MMAP feature",
            "type": "boolean"
        },
        "sparsemem": {
            "description": "sparse memory feature",
            "type": "boolean"
        },
        "clock_divisor": {
            "description": "clock divisor",
            "type": "integer"
        },
        "idlepc": {
            "description": "idle-pc value",
            "type": "string",
            "pattern": "^(0x[0-9a-fA-F]+)?$"
        },
        "idlemax": {
            "description": "idlemax value",
            "type": "integer",
        },
        "idlesleep": {
            "description": "idlesleep value",
            "type": "integer",
        },
        "exec_area": {
            "description": "exec area value",
            "type": "integer",
        },
        "jit_sharing_group": {
            "description": "JIT sharing group",
            "type": "integer",
        },
        "disk0": {
            "description": "disk0 size in MB",
            "type": "integer"
        },
        "disk1": {
            "description": "disk1 size in MB",
            "type": "integer"
        },
        "confreg": {
            "description": "configuration register",
            "type": "string",
            "minLength": 1,
            "pattern": "^0x[0-9a-fA-F]{4}$"
        },
        "console": {
            "description": "console TCP port",
            "type": "integer",
            "minimum": 1,
            "maximum": 65535
        },
        "aux": {
            "description": "auxiliary console TCP port",
            "type": "integer",
            "minimum": 1,
            "maximum": 65535
        },
        "mac_addr": {
            "description": "base MAC address",
            "type": "string",
            "minLength": 1,
            "pattern": "^([0-9a-fA-F]{4}\\.){2}[0-9a-fA-F]{4}$"
        },
        "system_id": {
            "description": "system ID",
            "type": "string",
            "minLength": 1,
        },
        "slot0": {
            "description": "Network module slot 0",
            "oneOf": [
                {"type": "string"},
                {"type": "null"}
            ]
        },
        "slot1": {
            "description": "Network module slot 1",
            "oneOf": [
                {"type": "string"},
                {"type": "null"}
            ]
        },
        "slot2": {
            "description": "Network module slot 2",
            "oneOf": [
                {"type": "string"},
                {"type": "null"}
            ]
        },
        "slot3": {
            "description": "Network module slot 3",
            "oneOf": [
                {"type": "string"},
                {"type": "null"}
            ]
        },
        "slot4": {
            "description": "Network module slot 4",
            "oneOf": [
                {"type": "string"},
                {"type": "null"}
            ]
        },
        "slot5": {
            "description": "Network module slot 5",
            "oneOf": [
                {"type": "string"},
                {"type": "null"}
            ]
        },
        "slot6": {
            "description": "Network module slot 6",
            "oneOf": [
                {"type": "string"},
                {"type": "null"}
            ]
        },
        "wic0": {
            "description": "Network module WIC slot 0",
            "oneOf": [
                {"type": "string"},
                {"type": "null"}
            ]
        },
        "wic1": {
            "description": "Network module WIC slot 0",
            "oneOf": [
                {"type": "string"},
                {"type": "null"}
            ]
        },
        "wic2": {
            "description": "Network module WIC slot 0",
            "oneOf": [
                {"type": "string"},
                {"type": "null"}
            ]
        },
        "startup_config_base64": {
            "description": "startup configuration base64 encoded",
            "type": "string"
        },
        "private_config_base64": {
            "description": "private configuration base64 encoded",
            "type": "string"
        },
        # C7200 properties
        "npe": {
            "description": "NPE model",
            "enum": ["npe-100",
                     "npe-150",
                     "npe-175",
                     "npe-200",
                     "npe-225",
                     "npe-300",
                     "npe-400",
                     "npe-g2"]
        },
        "midplane": {
            "description": "Midplane model",
            "enum": ["std", "vxr"]
        },
        "sensors": {
            "description": "Temperature sensors",
            "type": "array"
        },
        "power_supplies": {
            "description": "Power supplies status",
            "type": "array"
        },
        # I/O memory property for all platforms but C7200
        "iomem": {
            "description": "I/O memory percentage",
            "type": "integer",
            "minimum": 0,
            "maximum": 100
        },
    },
    "additionalProperties": False,
    "required": ["id"]
}

VM_START_CAPTURE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "Request validation to start a packet capture on a VM instance port",
    "type": "object",
    "properties": {
        "id": {
            "description": "VM instance ID",
            "type": "integer"
        },
        "port_id": {
            "description": "Unique port identifier for the VM instance",
            "type": "integer"
        },
        "slot": {
            "description": "Slot number",
            "type": "integer",
            "minimum": 0,
            "maximum": 6
        },
        "port": {
            "description": "Port number",
            "type": "integer",
            "minimum": 0,
            "maximum": 49  # maximum is 16 for regular port numbers, WICs port numbers start at 16, 32 or 48
        },
        "capture_file_name": {
            "description": "Capture file name",
            "type": "string",
            "minLength": 1,
        },
        "data_link_type": {
            "description": "PCAP data link type",
            "type": "string",
            "minLength": 1,
        },
    },
    "additionalProperties": False,
    "required": ["id", "port_id", "slot", "port", "capture_file_name"]
}

VM_STOP_CAPTURE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "Request validation to stop a packet capture on a VM instance port",
    "type": "object",
    "properties": {
        "id": {
            "description": "VM instance ID",
            "type": "integer"
        },
        "port_id": {
            "description": "Unique port identifier for the VM instance",
            "type": "integer"
        },
        "slot": {
            "description": "Slot number",
            "type": "integer",
            "minimum": 0,
            "maximum": 6
        },
        "port": {
            "description": "Port number",
            "type": "integer",
            "minimum": 0,
            "maximum": 49  # maximum is 16 for regular port numbers, WICs port numbers start at 16, 32 or 48
        },
    },
    "additionalProperties": False,
    "required": ["id", "port_id", "slot", "port"]
}

VM_SAVE_CONFIG_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "Request validation to save the configs for VM instance",
    "type": "object",
    "properties": {
        "id": {
            "description": "VM instance ID",
            "type": "integer"
        },
    },
    "additionalProperties": False,
    "required": ["id"]
}

VM_EXPORT_CONFIG_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "Request validation to export the configs for VM instance",
    "type": "object",
    "properties": {
        "id": {
            "description": "VM instance ID",
            "type": "integer"
        },
    },
    "additionalProperties": False,
    "required": ["id"]
}

VM_IDLEPCS_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "Request validation to calculate or show idle-pcs for VM instance",
    "type": "object",
    "properties": {
        "id": {
            "description": "VM instance ID",
            "type": "integer"
        },
        "compute": {
            "description": "indicates to compute new idle-pc values",
            "type": "boolean"
        },
    },
    "additionalProperties": False,
    "required": ["id"]
}

VM_ALLOCATE_UDP_PORT_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "Request validation to allocate an UDP port for a VM instance",
    "type": "object",
    "properties": {
        "id": {
            "description": "VM instance ID",
            "type": "integer"
        },
        "port_id": {
            "description": "Unique port identifier for the VM instance",
            "type": "integer"
        },
    },
    "additionalProperties": False,
    "required": ["id", "port_id"]
}

VM_ADD_NIO_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "Request validation to add a NIO for a VM instance",
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
            "description": "VM instance ID",
            "type": "integer"
        },
        "port_id": {
            "description": "Unique port identifier for the VM instance",
            "type": "integer"
        },
        "slot": {
            "description": "Slot number",
            "type": "integer",
            "minimum": 0,
            "maximum": 6
        },
        "port": {
            "description": "Port number",
            "type": "integer",
            "minimum": 0,
            "maximum": 49  # maximum is 16 for regular port numbers, WICs port numbers start at 16, 32 or 48
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
    "required": ["id", "port_id", "slot", "port", "nio"]
}

VM_DELETE_NIO_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "Request validation to delete a NIO for a VM instance",
    "type": "object",
    "properties": {
        "id": {
            "description": "VM instance ID",
            "type": "integer"
        },
        "slot": {
            "description": "Slot number",
            "type": "integer",
            "minimum": 0,
            "maximum": 6
        },
        "port": {
            "description": "Port number",
            "type": "integer",
            "minimum": 0,
            "maximum": 49  # maximum is 16 for regular port numbers, WICs port numbers start at 16, 32 or 48
        },
    },
    "additionalProperties": False,
    "required": ["id", "slot", "port"]
}
