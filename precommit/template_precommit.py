# Copyright (c) 2021-2022 by Cisco Systems, Inc.
# All rights reserved.

"""
This is a template for precommit scripts
Script documentation goes here
"""
from cisco.script_mgmt import precommit

def sample_method():
    """
    Method documentation
    """

    cfg = precommit.get_target_configs()
    # cfg = precommit.get_target_configs(format="sysdb") for target config in sysdb format

    # process and verify target configs here.

    precommit.config_warning("Print a warning message in commit report")
    precommit.config_error("Print an error message in commit report and abort commit operation")


if __name__ == '__main__':
    
    sample_method()