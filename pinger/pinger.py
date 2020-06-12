# Imports {{{
import requests
# }}}

def check_site(site):
    try:
        res = requests.get(site['url'], timeout=site['timeout'])
        if res.status_code != 200:
            return False
        return True
    except requests.exceptions.ConnectTimeout as cte:
        return False
    except Exception as e:
        return False

# vim: foldmethod=marker foldlevel=0
