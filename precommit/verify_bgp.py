# Copyright (c) 2021-2022 by Cisco Systems, Inc.
# All rights reserved.

"""
Script to verify if the target config has "router bgp" configurations
and if the bgp configs adhere to the rules
1. BGP AS in the range 123 to 234 is recommended
2. Remote AS of neighbours cannot be 25

"precommit" module APIs are used for
1. query target configs
2. Print warning messages in the commit output when minor config rule
   violations are found
3. Abort a commit operation when unpermitted config rule violations
   are found. 
Please look at cisco documentation for detailed documentation of this 
module

How to run:
1. Please follow README.MD to add and configure this precommit script.
2. Activate the script using config
    script precommit <script name> activate
    Example:
        script precommit verify_bgp.py activate
3. Configure any bgp config and commit the configs. The precommit
    script will be colled on commit operation and a report will be
    printed on status
    Example:
    !config for precommit test fail
    router bgp 100
     neighbor 1.2.3.4
      remote-as 25
     !
    !
    commit

    !Config for precommit test warning
    router bgp 100
     neighbor 1.2.3.4
      remote-as 26
     !
    !
    commit

    !Config for precommit test pass
    router bgp 200
     neighbor 1.2.3.4
      remote-as 26
     !
    !
    commit
"""

import re
from cisco.script_mgmt import xrlog
from cisco.script_mgmt import precommit

syslog = xrlog.getSysLogger('precommit_verify_bgp')
log = xrlog.getScriptLogger('precommit_verify_bgp')


def verify_bgp():
    """
    Query for target configs and check if the target configs has bgp configs adheres to
    the rules
    * Checks if the bgp AS is in the range 123-234
    * Checks if remote AS is not 25.  
    API precommit.get_target_configs will return the target configurations
    The target config can be queried in two formats . 
    1. CLI format
    2. sysdb format
    Both forms are shown below.
    :return: None on pass / Raise exception on failure.
    """

    # CLI verification
    cfg = precommit.get_target_configs()
    print(cfg)

    for cfg_line in cfg:

        bgp_cfg_start_pattern = re.match("^router bgp (.*)", cfg_line)
        if bgp_cfg_start_pattern:
            log.info("BGP config found")

            bgp_as = int(bgp_cfg_start_pattern.group(1))
            if not bgp_as in range(123, 234):
                precommit.config_warning("BGP AS number (%d) " % bgp_as +
                                         "not in recommended range (123-234)")

    # sysdb verification
    cfg = precommit.get_target_configs(format="sysdb")
    print(cfg)

    for item in cfg:

        remote_as_pattern = re.match("^gl/ip-bgp/default/0/.*/remote\-as", item.name)
        if remote_as_pattern:
            log.info("BGP remote AS config found")
            remote_as = int(item.value[1])
            if remote_as == 25:
                syslog.info("Attempt to configure BGP remote AS %d" % remote_as)
                precommit.config_error("Remote AS (%d) is not permitted" % remote_as)

    log.info("BGP verification is good")


if __name__ == '__main__':
    
    verify_bgp()

