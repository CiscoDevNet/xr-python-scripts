"""
This script gets the show route summary oper data and prints the total route operations.

To verify:
check for syslog 'Total route operations'
"""

import xmltodict
import re

from cisco.script_mgmt import xrlog
from iosxr.netconf.netconf_lib import *

syslog = xrlog.getSysLogger('test_netconf_show_ route_total')

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

    nc = NetconfClient(debug=True)
    nc.connect()
    do_get(nc, filter=filter_string)
    ret_dict = _xml_to_dict(nc.reply, 'rib')
    route_oper = int(ret_dict['rib']['rib-stats']['rib-stats-summary']['batch-stats']['route-op-arg-rx'])
    syslog.info('Total route operations: %s' %(route_oper))
    nc.close()
    
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
            syslog.error("ERROR: Get data is empty!")
            return False
    except Exception as e:
        syslog.error("Caught an Exception when performing get")
        return False


if __name__ == '__main__':

    syslog.info('Checking rib statistics')
    route_check()
