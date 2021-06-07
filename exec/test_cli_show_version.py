"""
This script executes show version on the router and prints the result.

Pre-requisite configuration:
aaa authorization exec default group tacacs+ local
aaa authorization eventmanager default local
aaa authentication login default group tacacs+ local

How to run?
script run exec <path> test_cli_show_version.py 

eg: script run /harddisk\: test_cli_show_version.py

Verify:
show logging last 10 
check for syslog: 'Show version successful'
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
