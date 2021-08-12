# Copyright (c) 2021 by Cisco Systems, Inc.
# All rights reserved.

"""
This script adds a loopback interface configuration.

To verify:
- Check configuraiton for the loopback interface
- Check syslog Configuration successful
"""
import argparse
import time
import json
import os
import xmltodict
import re


loopback = "Loopback123456"

from cisco.script_mgmt import xrlog
from iosxr.netconf.netconf_lib import NetconfClient

log = xrlog.getScriptLogger('Sample')
syslog = xrlog.getSysLogger('Sample')

def do_edit_cfg(nc, config=None, path=None):
    try:
        if path is not None:
            nc.rpc.edit_config(file=path)
        elif config is not None:
            nc.rpc.edit_config(config=config)
        else:
           syslog.error("ERROR: Config data is empty!")
           return False
    except Exception as e:
        syslog.error("Caught an Exception when editing config\n")
        syslog.error(str(e) + "\n")
        return False

    if "<ok/>" in nc.reply:
        return True
    else:
        return False


def do_commit(nc):
    try:
        nc.rpc.commit()
    except Exception as e:
        syslog.error("Caught Exception when committing config\n")
        return False


def config_interface():
    """
    Configure interface
    """
    edit_config = """
    <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
      <interface-configuration>
        <interface-name>%s</interface-name>
      </interface-configuration>
    </interface-configurations>
    """ % loopback

    # Initialize Netconf Connection
    nc = NetconfClient(debug=True)
    nc.connect()
    
    if do_edit_cfg(nc, config=edit_config):
        do_commit(nc)
        syslog.info("Configuration successful")

if __name__ == '__main__':
    config_interface()
