import requests


def check_site(site):
    try:
        res = requests.get(site['url'], timeout=site['timeout'])
        if res.status_code != 200:
            return False
        return True
    except Exception:
        return False
