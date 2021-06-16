# Copyright (c) 2021 by Cisco Systems, Inc.
# All rights reserved.
"""
This is a template for the config scripts 
"""

#Needed for config validation 
import cisco.config_validation as xr

#Used for generating syslogs
from cisco.script_mgmt import xrlog
syslog = xrlog.getSysLogger('Add script name here')

def check_config(root):
    #Add config validations
    pass
            
            
xr.register_validate_callback([<Add config path here>],check_config)
