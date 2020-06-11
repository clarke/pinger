#!/usr/bin/env python3

import requests

sites = [
    {
        'url': 'http://retzer.us',
        'timeout': 1,
    }
]

class StatusCodeException(Exception):
    pass

def check_site(site):
    try:
        res = requests.get(site['url'], timeout=site['timeout'])
        if res.status_code != 200:
            print(f"Status code: {res.status_code}")
            return False
        return True
    except Exception as e:
        print(f"Exception occurred: {e}")
        return False

if __name__ == "__main__":
    for site in sites:
        if not check_site(site):
            print(f"Check failed for {site['url']}")
        else:
            print(f"Successful check for {site['url']}")

