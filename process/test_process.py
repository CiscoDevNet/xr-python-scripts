"""
This checks the cpu utilization on the router at regular intervals and add syslogs.

""" 

import time
import os
import xmltodict
import re

from cisco.script_mgmt import xrlog
from iosxr.netconf.netconf_lib import *

log = xrlog.getScriptLogger('Sample')
syslog = xrlog.getSysLogger('Sample')

def cpu_memory_check():
    """
    Check total routes in router
    """
    '''
    filter_string = """
    <system-monitoring xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-wdsysmon-fd-oper">
     <cpu-utilization/>
    </system-monitoring>"""            
    nc = NetconfClient(debug=True)
    nc.connect()
    netconf_test_common.do_get(nc, filter=filter_string)
    ret_dict = _xml_to_dict(nc.reply, 'system-monitoring')
    print(ret_dict)
    nc.close()
    netconf_test_common.logf.close()
    '''
    cpu_utilization = [78,60,80,95]
    for cpu_util in cpu_utilization:
        if cpu_util >= 75:
            syslog.error("CPU utilization over 75%")
        else:
            syslog.info("CPU utilization normal")
        time.sleep(5)    
    
def _xml_to_dict(xml_output, xml_tag=None):
    """
    convert netconf rpc request to dict
    :param xml_output:
    :return:
    """
    if xml_tag:
        pattern = "<data>\s+(<%s.*</%s>).*</data>" % (xml_tag, xml_tag)
    else:
        pattern = "(<data>.*</data>)"   
    xml_output = xml_output.replace('\n', ' ')
    xml_data_match = re.search(pattern, xml_output)
    ret_dict = xmltodict.parse(xml_data_match.group(1))
    return ret_dict

def do_get(nc, filter=None, path=None):
    try:
        if path is not None:
            nc.rpc.get(file=path)
        elif filter is not None:
            nc.rpc.get(request=filter)
        else:
            print_log("ERROR: Get data is empty!\n")
            return False
    except Exception as e:
        print_log(str(e) + "\n")
        print_log(traceback.format_exc())
        print_log("Caught an Exception when performing get\n")
        return False
    return True

if __name__ == '__main__':
    cpu_memory_check()
