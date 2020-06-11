#!/usr/bin/env python3

# Imports {{{
import requests
import yaml
from pathlib import Path
import os
# }}}

# Configuration {{{
configuration_file = '~/.pinger.conf'
# }}}

# Custom Exceptions {{{
class StatusCodeException(Exception):
    pass
# }}}

def get_configuration():
    with open(Path(os.path.expanduser('~/.pinger.conf'))) as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)
    return conf

def check_site(site):
    try:
        res = requests.get(site['url'], timeout=site['timeout'])
        if res.status_code != 200:
            print(f"Status code: {res.status_code}")
            return False
        return True
    except requests.exceptions.ConnectTimeout as cte:
        print(f"Connection timeout for {site['url']}")
    except Exception as e:
        print(f"Exception occurred: {e}")
        return False

if __name__ == "__main__": # {{{
    configuration = get_configuration()

    for site in configuration['sites'].keys():
        if not check_site(configuration['sites'][site]):
            print(f"Check failed for {site}")
        else:
            print(f"Successful check for {site}")
# }}}

# vim: foldmethod=marker foldlevel=0
