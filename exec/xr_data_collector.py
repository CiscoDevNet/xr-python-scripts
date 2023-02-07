# Copyright (c) 2021-2022 by Cisco Systems, Inc.
# All rights reserved.
import logging
import xmltodict
import re

log = logging.getLogger("xr_data_collector")

RE_INTF_PATTERN = r'(^[A-Za-z\-]+)([0-9\./]*)'


def get_controller_stats(nc_con):
    """
    Does a netconf query of the controller stats of interfaces in device. A list
    of dictionary is generated with each dict storing the stats for one interface
    This list of dictionaries is returned.
    Yang path: Cisco-IOS-XR-drivers-media-eth-oper:ethernet-interface/statistics/statistic
    :param nc_con: Netconf connection object
    :return: list of dictionaries . each dict has stats for one interface
    """
    ret_list = list()

    yang_filter = """
      <ethernet-interface xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-drivers-media-eth-oper">
        <statistics>
          <statistic/>
        </statistics>
      </ethernet-interface>
    """
    try:
        nc_con.rpc.get(request=yang_filter)
    except Exception as err:
        log.exception('Error during netconf get \n filter: {yang_filter}\n '
                      'Error : {err}'.format(yang_filter=yang_filter, err=err))
        raise err
    reply_dict = netconf_xml_to_dict(nc_con.reply, xml_tag='ethernet-interface')

    for reply_int_dict in reply_dict['ethernet-interface']['statistics']['statistic']:
        ret_list.append(reply_int_dict)
    return ret_list


def get_controller_interface_stats(nc_con):
    """
    Does a netconf query of the controller inteface stats of interfaces in device. A list
    of dictionary is generated with each dict storing the stats for one interface
    This list of dictionaries is returned.
    Yang path: Cisco-IOS-XR-drivers-media-eth-oper:ethernet-interface/interfaces/interface
    :param nc_con: Netconf connection object
    :return: list of dictionaries . each dict has stats for one interface
    """
    ret_list = list()

    yang_filter = """
      <ethernet-interface xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-drivers-media-eth-oper">
        <interfaces>
          <interface/>
        </interfaces>
      </ethernet-interface>
    """
    try:
        nc_con.rpc.get(request=yang_filter)
    except Exception as err:
        log.exception('Error during netconf get \n filter: {yang_filter}\n '
                      'Error : {err}'.format(yang_filter=yang_filter, err=err))
        raise err
    reply_dict = netconf_xml_to_dict(nc_con.reply, xml_tag='ethernet-interface')

    for reply_int_dict in reply_dict['ethernet-interface']['interfaces']['interface']:
        ret_list.append(reply_int_dict)
    return ret_list


def get_controller_npu_interfaces_stats(nc_con):
    """
    Does a netconf query of the npu stats of interface on device. A list
    of dictionary is generated with each dict storing the stats for one interface
    This list of dictionaries is returned.
    Yang path : Cisco-IOS-XR-ofa-npu-stats-oper:ofa/stats/nodes/node/npu-numbers/
                npu-number/display/interface-handles/interface-handle
    :param nc_con: Netconf connection object
    :return: list of dictionaries . each dict has stats for one interface
    """
    ret_list = list()

    yang_filter = """
      <ofa xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ofa-npu-stats-oper">
        <stats>
          <nodes>
            <node>
              <npu-numbers>
                <npu-number>
                  <display>
                    <fair-voq-base-numbers/>
                    <interface-handles>
                      <interface-handle/>
                    </interface-handles>
                  </display>
                </npu-number>
              </npu-numbers>
            </node>
          </nodes>
        </stats>
      </ofa>
    """
    try:
        nc_con.rpc.get(request=yang_filter)
    except Exception as err:
        log.exception('Error during netconf get \n filter: {yang_filter}\n '
                      'Error : {err}'.format(yang_filter=yang_filter, err=err))
        raise err
    reply_dict = netconf_xml_to_dict(nc_con.reply, xml_tag='nodes')

    if type(reply_dict['nodes']['node']) != list:
        # distributed systems single LCs
        if type(reply_dict['nodes']['node']['npu-numbers']['npu-number']) != list:
            # fixed systems
            reply_dict['nodes']['node']['npu-numbers']['npu-number'] = \
                [reply_dict['nodes']['node']['npu-numbers']['npu-number']]

        reply_dict['nodes']['node'] = [reply_dict['nodes']['node']]

    ret_list = reply_dict['nodes']['node']
    return ret_list


def get_interfaces_status(nc_con):
    """
    Does a netconf query of the interface status on device. A list
    of dictionary is generated with each dict storing the stats for one interface
    This list of dictionaries is returned
    Yang path: Cisco-IOS-XR-pfi-im-cmd-oper:interfaces/interface-xr/interface
    :param nc_con: Netconf connection object
    :return: list of dictionaries . each dict has stats for one interface
    """
    ret_list = list()

    yang_filter = """
      <interfaces xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-pfi-im-cmd-oper">
        <interface-xr>
          <interface/>
        </interface-xr>
      </interfaces>
    """
    try:
        nc_con.rpc.get(request=yang_filter)
    except Exception as err:
        log.exception('Error during netconf get \n filter: {yang_filter}\n '
                      'Error : {err}'.format(yang_filter=yang_filter, err=err))
        raise err
    reply_dict = netconf_xml_to_dict(nc_con.reply, xml_tag='interfaces')

    for reply_int_dict in reply_dict['interfaces']['interface-xr']['interface']:
        ret_list.append(reply_int_dict)
    return ret_list


def get_controller_npu_traps_stats(nc_con):
    """
    Does a netconf query of the npu stats for all traps on device. A list
    of dictionary is generated with each dict storing the stats for one trap
    This list of dictionaries is returned.
    Yang path : Cisco-IOS-XR-ofa-npu-stats-oper:ofa/stats/nodes/node/
                npu-numbers/npu-number/display/trap-ids/trap-id
    :param nc_con: Netconf connection object
    :return: list of dictionaries . each dict has stats for one interface
    """
    ret_list = list()

    yang_filter = """
      <ofa xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ofa-npu-stats-oper">
        <stats>
          <nodes>
            <node>
              <npu-numbers>
                <npu-number>
                  <display>
                    <trap-ids>
                      <trap-id/>
                    </trap-ids>
                  </display>
                </npu-number>
              </npu-numbers>
            </node>
          </nodes>
        </stats>
      </ofa>
    """
    try:
        nc_con.rpc.get(request=yang_filter)
    except Exception as err:
        log.exception('Error during netconf get \n filter: {yang_filter}\n '
                      'Error : {err}'.format(yang_filter=yang_filter, err=err))
        raise err
    reply_dict = netconf_xml_to_dict(nc_con.reply, xml_tag='nodes')

    if type(reply_dict['nodes']['node']) == list:
        # distributed systems multiple LCs
        node_list = reply_dict['nodes']['node']
    else:
        node_list = [reply_dict['nodes']['node']]

    for node in node_list:
        if type(node['npu-numbers']['npu-number']) == list:
            npu_list = node['npu-numbers']['npu-number']
        else:
            npu_list = [node['npu-numbers']['npu-number']]
        for npu in npu_list:
            for int_stats in npu['display']['trap-ids']['trap-id']:
                int_stats['node-name'] = node['node-name']
                ret_list.append(int_stats)
    return ret_list


def get_hardware_drops(cli_handle):
    """
    Does a CLI query of the drops data on device. A list of
    dictionary is generated with each dictionary have data for one drop type
    This list of dictionaries is returned
    CLI used : show drops all ongoing location all
    :param cli_handle: XR CLI helper handle
    :return: dictionary
    """
    ret_list = list()
    node_pattern = r"^Printing Drop Counters for node ([^\s]+)/CPU0$"
    trap_pattern = r".*\s+[0-9]\s+[0-9]+\s+.*[0-9]+\s+[0-9]+\s+[0-9]+$"
    try:
        cmd = 'show drops all ongoing location all'
        result = cli_handle.xrcli_exec(cmd)
    except Exception as err:
        log.exception('Error during CLI (cmd) execution'
                      'Error : {err}'.format(cmd=cmd, err=err))
        raise err

    if not result['status'] == 'success':
        raise Exception('Execution of CLI {cmd} not successful.'.format(cmd=cmd))

    node = ''
    for line in result['output'].split('\n'):

        node_match = re.match(node_pattern, line)
        if node_match:
            node = node_match.group(1)

        if node:
            trap_match = re.match(trap_pattern, line)

            trap_values = line[46:].split()
            if trap_match and len(trap_values) == 12:
                trap_dict = {'node-name': node}
                trap_dict['trap-type'] = line[0:46].strip()
                trap_dict['npu-id'] = trap_values[0]
                trap_dict['trap-id'] = trap_values[1]
                trap_dict['punt-destination'] = trap_values[2]
                trap_dict['punt-voq'] = trap_values[3]
                trap_dict['punt-vlan'] = trap_values[4]
                trap_dict['punt-tc'] = trap_values[5]
                trap_dict['configured-rate'] = trap_values[6]
                trap_dict['hardware-rate'] = trap_values[7]
                trap_dict['policer-level'] = trap_values[8]
                trap_dict['average-packet-size'] = trap_values[9]
                trap_dict['packets-accepted'] = trap_values[10]
                trap_dict['packets-dropped'] = trap_values[11]
                ret_list.append(trap_dict)
    return ret_list


def get_interface_policy_map(cli_handle):
    """
    Does a CLI query of policy-map stats of interfaces on device. A list of
    dictionary is generated with each dictionary have data for one interface
    This list of dictionaries is returned
    CLI used : show policy-map all interface all
    :param cli_handle: XR CLI helper handle
    :return: dictionary
    """
    ret_list = list()
    class_pattern = r'^Class (\S+)'
    tx_pattern = r'^\s+Transmitted\s+:\s+([0-9]+)/([0-9]+)\s+([0-9]+)'
    total_pattern = r'^\s+Total Dropped\s+:\s+([0-9]+)/([0-9]+)\s+([0-9]+)'
    ecn_marked_pattern = r'^\s+RED ecn marked & transmitted\(packets/bytes\):\s+([0-9]+)/([0-9]+)'
    try:
        cmd = 'show policy-map interface all'
        result = cli_handle.xrcli_exec(cmd)
    except Exception as err:
        log.exception('Error during CLI (cmd) execution'
                      'Error : {err}'.format(cmd=cmd, err=err))
        raise err

    if not result['status'] == 'success':
        raise Exception('Execution of CLI {cmd} not successful.'.format(cmd=cmd))

    intf_dict = dict()
    for line in result['output'].split('\n'):

        intf_match = re.match(RE_INTF_PATTERN + r'\s+(input|output):\s+(\S+)', line)
        if intf_match:

            for intf_dict in ret_list:
                if intf_dict['interface-name'] == intf_match.group(1)+intf_match.group(2):
                    break
            else:
                intf_dict = {'interface-name': intf_match.group(1)+intf_match.group(2),
                             'input-rates': list(), 'output-rates': list(),
                             'input-policy-name': '', 'output-policy-name': ''}
                ret_list.append(intf_dict)
            direction = intf_match.group(3)
            intf_dict[direction + '-policy-name'] = intf_match.group(4)

        class_match = re.match(class_pattern, line)
        if class_match and intf_dict:
            class_dict = {'class-name': class_match.group(1)}
            intf_dict[direction + '-rates'].append(class_dict)

        tx_match = re.match(tx_pattern, line)
        if tx_match and class_dict:
           class_dict['transmitted-packets'] = tx_match.group(1)
           class_dict['transmitted-bytes'] = tx_match.group(2)
           class_dict['transmitted-rate'] = tx_match.group(3)

        total_match = re.match(total_pattern, line)
        if total_match and class_dict:
            class_dict['total-dropped-packets'] = total_match.group(1)
            class_dict['total-dropped-bytes'] = total_match.group(2)
            class_dict['total-dropped-rate'] = total_match.group(3)

        ecn_marked_match = re.match(ecn_marked_pattern, line)
        if ecn_marked_match and class_dict:
            class_dict['ecn-marked-transmitted-packets'] = ecn_marked_match.group(1)
            class_dict['ecn-marked-transmitted-bytes'] = ecn_marked_match.group(2)
    return ret_list


def get_interface_name_handle_mapping(cli_handle):
    """
    Does a CLI query of the interface database on device. A
    dictionary is generated with key as the handle and the value as interface name
    This dictionary is returned
    CLI used : show im database brief location all
    :param cli_handle: XR CLI helper handle
    :return: dictionary
    """
    ret_dict = dict()
    try:
        cmd = 'show im database brief location all'
        result = cli_handle.xrcli_exec(cmd)
    except Exception as err:
        log.exception('Error during CLI (cmd) execution'
                      'Error : {err}'.format(cmd=cmd, err=err))
        raise err

    if not result['status'] == 'success':
        raise Exception('Execution of CLI {cmd} not successful.'.format(cmd=cmd))
    for line in result['output'].split('\n'):
        split_line = line.split(' ')
        if split_line[0].startswith('0x'):
            ret_dict[split_line[0]] = split_line[1]
    return ret_dict


def netconf_xml_to_dict(xml_output, xml_tag=None):
    """
    Converts netconf rpc request reply into a dict
    :param xml_output: netconf reply xml data structure
    :param xml_tag: xml_tags enclosing the data to be parsed.
                    "data" tag is used if empty.
    :return: dictionary equivalent of xml passed
    """
    if xml_tag:
        pattern = '<data.*?>.*?(<%s.*?>.*</%s>).*</data>' % (xml_tag, xml_tag)
    else:
        pattern = '(<data>.*</data>)'
    xml_output = xml_output.replace('\n', ' ')
    xml_data_match = re.search(pattern, xml_output)
    ret_dict = xmltodict.parse(xml_data_match.group(1))
    return ret_dict


def get_interface_rsmp(intf):
    """
    Function to extract the rack , slot, module, port information from an interfaces name
    and return a list of intergers repsenting the rack , slot , module , port etc
    This is used for sorting a list interfaces
    :param intf: Interface name
    :return: list of integers
    """
    rsmp = list()
    for item in re.split(r'/|\.', intf):
        try:
            rsmp_match = re.match(r'^[A-Za-z]*([0-9\.]+)', item)
            rsmp.append(int(rsmp_match.group(1)))
        except:
            rsmp.append(0)
    return rsmp


def is_ignore_interface(interface_name):
    """
    Return true if the interface should be ignored like Mgmt or PTP
    :param inteface_name: Name of interface
    :return:
    """
    return ('MgmtEth' in interface_name or
            'PTP' in interface_name)


def gen_interface_type_name(bandwidth=0, name='', name_format='name'):
    """
    Generate the interface type name for the bandwidth passed.
    :param bandwidth:  Bandwidth in kb
    :param name:  name of the interface
    :param name_format: [full,name,short] format of the name returned
    :return:
    """
    names = dict()
    rmsp = ''
    if name:
        match = re.search(RE_INTF_PATTERN, name)
        if match:
            name_type = match.group(1).lower()
            rsmp = match.group(2)
        else:
            raise Exception('Invalid interface name ({name}) passed as argument'.format(name=name))

    if int(bandwidth) == 1000000 or \
        name_type == "gige":
        names['full'] = "GigabitEthernet"
        names['name'] = "GigE"
        names['short'] = "Gi"
    elif int(bandwidth) == 10000000 or \
            name_type == "tengige":
        names['full'] = "TenGigabitEthernet"
        names['name'] = "TenGigE"
        names['short'] = "Te"
    elif int(bandwidth) == 25000000 or \
            name_type == "twentyfivegige":
        names['full'] = "TwentyFiveGigabitEthernet"
        names['name'] = "TwentyFiveGigE"
        names['short'] = "TF"
    elif int(bandwidth) == 40000000 or \
            name_type == "fortygige":
        names['full'] = "FortyGigabitEthernet"
        names['name'] = "FortyGigE"
        names['short'] = "Fo"
    elif int(bandwidth) == 50000000 or \
            name_type == "fiftygige":
        names['full'] = "FiftyGigabitEthernet"
        names['name'] = "FiftyGigE"
        names['short'] = "Fi"
    elif int(bandwidth) == 100000000 or \
            name_type == "hundredgige":
        names['full'] = "HundredGigabitEthernet"
        names['name'] = "HundredGigE"
        names['short'] = "Hu"
    elif int(bandwidth) == 200000000 or \
            name_type == "twohundredgige":
        names['full'] = "TwoHundredGigabitEthernet"
        names['name'] = "TwoHundredGigE"
        names['short'] = "TH"
    elif int(bandwidth) == 400000000 or \
            name_type == "fourhundredgige":
        names['full'] = "FourHundredGigabitEthernet"
        names['name'] = "FourHundredGigE"
        names['short'] = "FH"
    elif int(bandwidth) == 800000000 or \
            name_type == "eighthundredgige":
        names['full'] = "EightHundredGigabitEthernet"
        names['name'] = "EightHundredGigE"
        names['short'] = "EH"
    else:
        if name:
            raise Exception('Invalid interface name ({name}) passed as argument'.format(name=name))
        else:
            raise Exception('Unknown interface bandwidth: {bw}'.format(bw=int(bandwidth)))

    if name_format in ['full', 'name', 'short']:
        return names[name_format]+rsmp
    else:
        raise Exception('Invalid value for name_format. valid values are full,name, or short')
