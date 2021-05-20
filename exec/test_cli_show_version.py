"""
This script shuts down an interface specified by the user via CLI option

How to run?
script run exec <path> test_xr_config.py <interface>

eg: script run /harddisk\: test_xr_config.py Hu0/0/0/35

Configuration: 
interface <interface>
shutdown

Verify:
show logging last 10 
check for syslog: 'SCRIPT : Configuration succeeded'
""" 
import argparse
import time
import sys
import os
import pprint
from iosxr.xrcli.xrcli_helper import *
from cisco.script_mgmt import xrlog

logger = xrlog.getScriptLogger('sample_script')
syslog = xrlog.getSysLogger('sample_script')
helper = XrcliHelper(debug = True)

if __name__ == '__main__':
        cmd = "show version"
        result = helper.xrcli_exec(cmd)
        print(result)
        if result['status'] == 'success':
            syslog.info('SCRIPT : Show version successful')
        else:
            syslog.error('SCRIPT : Show version failed')   
