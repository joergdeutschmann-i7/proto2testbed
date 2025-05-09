#
# This file is part of Proto²Testbed.
#
# Copyright (C) 2024 Martin Ottens
# 
# This program is free software: you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License 
# along with this program. If not, see https://www.gnu.org/licenses/.
#

import json

from enum import Enum
from typing import Dict, List, Any, Optional

from common.application_configs import ApplicationConfig
from common.interfaces import JSONSerializer


class InstanceMessageType(Enum):
    STARTED = "started"
    INITIALIZED = "initialized"
    DATA_POINT = "data_point"
    MSG_SUCCESS = "msg_success"
    MSG_INFO = "msg_info"
    MSG_WARNING = "msg_warning"
    MSG_DEBUG = "msg_debug"
    MSG_ERROR = "msg_error"
    FAILED = "failed"
    APPS_INSTALLED = "apps_installed"
    APPS_FAILED = "apps_failed"
    APPS_DONE = "apps_done"
    FINISHED = "finished"
    COPIED_FILE = "copied_file"
    SHUTDOWN = "shutdown"
    UNKNOWN = "unknown"

    def __str__(self):
        return str(self.value)
    
    @staticmethod
    def from_str(status: str):
        try: return InstanceMessageType(status)
        except Exception:
            return InstanceMessageType.UNKNOWN
        
        
class JSONSerializable():
    def as_json_bytes(self) -> bytes:
        return json.dumps(vars(self)).encode("utf-8")


class JSONSerializable():
    def as_json_bytes(self) -> bytes:
        return json.dumps(vars(self)).encode("utf-8")

# Downstream: Instance -> Controller
# Upstream:   Controller -> Instance

class InstanceManagerDownstream(JSONSerializer):
    def __init__(self, name: str, status: str, message: Any = None):
        self.name = name
        self.status = status
        self.message = message
    
    def get_status(self) -> InstanceMessageType:
        return InstanceMessageType.from_str(self.status)


class InitializeMessageUpstream(JSONSerializer):
    status_name =  "initialize"

    def __init__(self, script: str, environment: Dict[str, str], status = None):
        self.status = InitializeMessageUpstream.status_name
        self.script = script
        self.environment = environment


class InstallApplicationsMessageUpstream(JSONSerializer):
    status_name = "install_apps"

    def __init__(self, applications: Optional[List[ApplicationConfig]] = None, 
                 status = None) -> None:
        self.status = InstallApplicationsMessageUpstream.status_name
        self.applications = applications

    @staticmethod
    def from_json(json):
        obj = InstallApplicationsMessageUpstream(**json)

        if obj.applications is None:
            return obj
        
        obj.applications = []
        for application in json["applications"]:
            obj.applications.append(ApplicationConfig(**application))

        return obj


class RunApplicationsMessageUpstream(JSONSerializer):
    status_name = "run_apps"

    def __init__(self, status = None):
        self.status = RunApplicationsMessageUpstream.status_name
    

class CopyFileMessageUpstream(JSONSerializer):
    status_name = "copy"

    def __init__(self, source: str, target: str, source_renameto: str, proc_id: str, status=None):
        self.status = CopyFileMessageUpstream.status_name
        self.source = source
        self.source_renameto = source_renameto
        self.target = target
        self.proc_id = proc_id


class FinishInstanceMessageUpstream(JSONSerializer):
    status_name = "finish"

    def __init__(self, preserve_files: Optional[List[str]] = None, do_preserve: bool = True, status = None):
        self.status = FinishInstanceMessageUpstream.status_name
        self.preserve_files = preserve_files
        self.do_preserve = do_preserve

