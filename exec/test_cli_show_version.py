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
