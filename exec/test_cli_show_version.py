# Copyright (c) 2021 by Cisco Systems, Inc.
# All rights reserved.

"""
This script executes show version on the router and prints the result.

Verify:
check for syslog: 'Show version successful'
""" 
import argparse
import time
import sys
import os
import pprint
from iosxr.xrcli.xrcli_helper import *
from cisco.script_mgmt import xrlog


syslog = xrlog.getSysLogger('test_cli_show_version')
helper = XrcliHelper(debug = True)

def test_execute():
        cmd = "show version"
        result = helper.xrcli_exec(cmd)
        print(result)
        if result['status'] == 'success':
            syslog.info('SCRIPT : Show version successful')
        else:
            syslog.error('SCRIPT : Show version failed')   

if __name__ == '__main__':
        test_execute()
       

