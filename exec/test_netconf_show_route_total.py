import argparse
import time
import json
import os
import xmltodict
import re
import netconf_test_common

from cisco.script_mgmt import xrlog
from iosxr.netconf.netconf_lib import *

log = xrlog.getScriptLogger('Sample')
syslog = xrlog.getSysLogger('Sample')
LOG_FILE = "netconf_oper_1_" + str(os.getpid()) + ".txt"

def route_check():
    """
    Check total routes in router
    """
    logfile = netconf_test_common.DEFAULT_LOG_PATH + LOG_FILE
    filter_string = """
    <rib xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ip-rib-ipv4-oper">
    <rib-stats>
    <rib-stats-summary/>
    </rib-stats>
    </rib>"""            
    try:
        netconf_test_common.logf = open(logfile, 'w')
    except Exception as e:
        print("ERROR: Unable to open " + logfile + "!")
        return None
    nc = NetconfClient(debug=True)
    nc.connect()
    netconf_test_common.do_get(nc, filter=filter_string)
    ret_dict = _xml_to_dict(nc.reply, 'rib')
    route_oper = int(ret_dict['rib']['rib-stats']['rib-stats-summary']['batch-stats']['route-op-arg-rx'])
    syslog.info('Total route operations: %s' %(route_oper))
    nc.close()
    netconf_test_common.logf.close()
    
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


if __name__ == '__main__':

    syslog.info('Checking rib statistics')
    route_check()
