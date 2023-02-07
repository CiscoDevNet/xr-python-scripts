# Copyright (c) 2021-2022 by Cisco Systems, Inc.
# All rights reserved.

"""
Script to generate a systemic view of interface queue ecn counters .

This script queries queries on the interface stats of
the interfaces on the device and store the data into
a list of dictionaries. Then a table having the ecn counters per queue
of each interface is printed.

usage: show_interfaces_counters_ecn.py [{text,json}]

Arguments:
  text/json             [text] Format of report to generate.
ios#script run show_interfaces_counters_ecn.py
ios#script run show_interfaces_counters_ecn.py arguments json
ios#script run show_interfaces_counters_ecn.py arguments text
"""

import argparse
import json
import traceback
import sys
from collections import OrderedDict
from iosxr.xrcli.xrcli_helper import XrcliHelper
from cisco.script_mgmt import xrlog
from cisco.script_mgmt import xr_utils
# import xr_data_collector
xr_data_collector = xr_utils.secure_import(module_file_name="xr_data_collector.py")

log = xrlog.getScriptLogger('show_interfaces_counters_ecn')


def generate_show_interfaces_counters_ecn_report(int_stats_list, report_format):
    """
    Generate a table of  interface queue ecn counters
    :param int_stats_list:  List of dicts . Each dict has the interface
                                        Stats for one interface
    :param report_format: ["text"/"json"] . report format to be retuend
    :return: Report in text/json format having input and output tables
    """

    col_names = [
                'Interface',
                'Class',
                'Marked Pkts',  'Marked Bytes',
                ]
    keys =      [
                'interface-name',
                'class-name',
                'ecn-marked-transmitted-packets', 'ecn-marked-transmitted-bytes',
                ]

    if report_format == "text":
        cwidth = dict(); calign = dict()
        cwidth['Interface'] = 16
        calign['Interface'] = '<'
        cwidth['Class'] = 30
        calign['Class'] = '<'
        cwidth['Marked Pkts'] = 20
        calign['Marked Pkts'] = '>'
        cwidth['Marked Bytes'] = 20
        calign['Marked Bytes'] = '>'
        table_len = sum(cwidth.values()) + 4
        sline = '-' * table_len

        header = ''
        for col_name in col_names:
            header += '{:{align}{width}}'.format(col_name, align=calign[col_name], width=cwidth[col_name])
        in_stats_lines = out_stats_lines = ''
    elif report_format == "json":
        rep_list = list()

    for int_stats in sorted(int_stats_list,
                            key=lambda item: xr_data_collector.get_interface_rsmp(item['interface-name'])):

        if xr_data_collector.is_ignore_interface(int_stats['interface-name']):
            # ignore management interfaces
            continue

        try:
            int_name = xr_data_collector.gen_interface_type_name(name=int_stats['interface-name'],
                                                                 name_format='short')
        except:
            # ignore invalid interfaces
            continue

        out_stats_line = ''
        ret_int_dict = OrderedDict()
        ret_int_dict['interface-name'] = int_name
        ret_int_dict['output-rates'] = []
        for class_stats in int_stats['output-rates']:

            if "ecn-marked-transmitted-packets" not in class_stats:
                continue
            if report_format == "text":
                out_stats_line = '{:{align}{width}}'.format(int_name,
                                                            align=calign['Interface'], width=cwidth['Interface'])
            elif report_format == "json":
                class_dict = OrderedDict()

            for (key_name, col_name) in zip(keys[1:], col_names[1:]):
                val = class_stats[key_name]
                if report_format == "text":
                    out_stats_line += '{:{align}{width}}'.format(val,
                                                                 align=calign[col_name], width=cwidth[col_name])
                elif report_format == "json":
                    class_dict[key_name] = val

            if report_format == "text":
                out_stats_lines += out_stats_line + '\n'
            elif report_format == "json":
                ret_int_dict['output-rates'].append(class_dict)
        if report_format == "json":
            rep_list.append(ret_int_dict)

    if report_format == "text":

        rep = sline + '\n'
        rep += header + '\n'
        rep += sline + '\n'
        rep += out_stats_lines
        rep += sline + '\n'
    elif report_format == "json":
        rep = json.dumps(rep_list, indent=4, sort_keys=False)
    else:
        rep = "Invalid report format"

    return rep


if __name__ == '__main__':

    try:
        # command line parameters parsing
        parser = argparse.ArgumentParser()
        parser.add_argument('report_format',
                            help='[text/json] Format of report to generate.',
                            default='text',
                            nargs='?'
                            )
        args = parser.parse_args()

        # start xr cli helper session on router
        log.debug('Starting CLI helper session')
        cli_handle = XrcliHelper()

        # get int policy map stats for all the interfaces
        log.debug('Collecting policy map stats from the router')
        int_q_stats_list = xr_data_collector.get_interface_policy_map(cli_handle)

        # generate and print report
        log.debug('Generating report')
        report = generate_show_interfaces_counters_ecn_report(int_q_stats_list,
                                                              args.report_format)
        log.debug('Printing report')
        print(report, flush=True)

    except Exception as err:
        log.debug("Script error: {err}".format(err=traceback.format_exc()))
        print('! Script error : {err}'.format(err=str(err)))
        sys.exit(1)
