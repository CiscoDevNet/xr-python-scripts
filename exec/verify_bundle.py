# Copyright (c) 2021-2022 by Cisco Systems, Inc.
# All rights reserved.

"""
Bundle interfaces bandwidth verification script

Verify bundle interfaces mpls packets per sec is below threshold.
If pkts/sec is greater than threshold then print syslog message
and add list of new interfaces to bundle

How to run:
Please follow README.MD to add and configure this exec script.
Use "script run" CLI or netconf equivalentto run the script
script run <script name> arguments <script arguments>
Example:
RP/0/RP0/CPU0:ios#script run verify_bundle.py arguments '--name' 'Bundle-Ether6432'
                  '-t' '400000' '-m' 'FourHundredGigE0/0/0/2, FourHundredGigE0/0/0/3

Note: AAA configurations are required for xrcli_helper module to work
This module provides API's to execute and configure IOS-XR cli commands. 
Example:
aaa authorization exec default group tacacs+ local
aaa authorization eventmanager default local
aaa authentication login default group tacacs+ local

Arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Bundle interface name
  -t THRESHOLD, --threshold THRESHOLD
                        Bandwidth threshold
  -m MEMBERS, --members MEMBERS
                        interfaces (coma separated) to add to bundle
"""
import re
import argparse
from iosxr.xrcli.xrcli_helper import XrcliHelper
from cisco.script_mgmt import xrlog

syslog = xrlog.getSysLogger('verify_bundle')
log = xrlog.getScriptLogger('verify_bundle')


def add_bundle_members(bundle_name, members):
    """
    Add new members to a bundle
    :param bundle_name: Name of the bundle
    :param members: Name of member interfaces to add to bundle
    :return: None on success / raises exception on failure
    """

    helper = XrcliHelper()
    bundle_pattern = re.compile('[A-Z,a-z, ]([0-9]+)')
    match = bundle_pattern.search(bundle_name)
    if match:
        bundle_id = match.group(1)
    else:
        raise Exception('Invalid bundle name')
    cfg = ''
    for member in members:

        cfg = cfg + 'interface %s \nbundle id %s mode active\nno shutdown\n' % \
              (member.strip(), bundle_id)

    log.info("Configs to be added : \n%s" % cfg)
    result = helper.xr_apply_config_string(cfg)
    if result['status'] == 'success':
        msg = "Configuring new bundle members successful"
        syslog.info(msg)
        log.info(msg)
    else:
        msg = "Configuring new bundle members failed"
        syslog.warning(msg)
        log.warning(msg)


def verify_bundle(bundle_name, threshold):
    """
    Verify if the bandwidth usage of a bundle is above the provided threshold
    :param bundle_name:  Name of bundle to verify
    :param threshold: bundle bandwidth used threshold in pps
    :return: True if the bundle bandwidth used is below the threshold passed
             False otherwise
    """

    helper = XrcliHelper()
    cmd = "show interfaces %s accounting rates" % bundle_name
    cmd_out = helper.xrcli_exec(cmd)
    if not cmd_out['status'] == 'success':
        raise Exception('Invalid bundle or error getting interface accounting rates')

    log.info('Command output : \n%s' % cmd_out['output'])
    rate_pattern = re.compile("MPLS +[0-9]+ +[0-9]+ +[0-9]+ +([0-9]+)")
    match = rate_pattern.search(cmd_out['output'])
    if match:
        pktspersec = int(match.group(1))
        if pktspersec > int(threshold):
            msg = 'Bundle %s bandwidth of %d pps is above threshold of %s pps' % \
                    (bundle_name, pktspersec, threshold)
            log.info(msg)
            syslog.info(msg)
            return False
        else:
            msg = 'Bundle %s bandwidth of %d pps is below threshold of %s pps' % \
                    (bundle_name, pktspersec, threshold)
            log.info(msg)
            return True


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Verify budle")
    parser.add_argument("-n", "--name",
                        help="Bundle interface name")
    parser.add_argument("-t", "--threshold",
                        help="Bandwidth threshold")
    parser.add_argument("-m", "--members",
                        help="interfaces (coma separated) to add to bundle")
    args = parser.parse_args()
    log.info('Script arguments :')
    log.info(args)
    if not verify_bundle(args.name, args.threshold):
        syslog.info("Adding new members (%s) to bundle interfaces %s" %
                    (args.members, args.name))
        add_bundle_members(args.name, args.members.split(','))
