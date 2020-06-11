# Imports {{{
import requests
# }}}

def check_site(site):
    try:
        res = requests.get(site['url'], timeout=site['timeout'])
        if res.status_code != 200:
            print(f"Status code: {res.status_code}")
            return False
        return True
    except requests.exceptions.ConnectTimeout as cte:
        return False
    except Exception as e:
        print(f"Exception occurred: {e}")
        return False

# vim: foldmethod=marker foldlevel=0
