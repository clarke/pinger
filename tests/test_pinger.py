from pinger import pinger
import responses
from requests.exceptions import ConnectTimeout


def test_check_site_not_found():
    url = 'https://fake.url/'

    site = {
        'url':     url,
        'timeout': 1,
    }

    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(responses.GET, url, status=404)
        res = pinger.check_site(site)
        assert res is False


def test_check_site_success():
    url = 'https://fake.url/'
    site = {
        'url':     url,
        'timeout': 1,
    }

    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(responses.GET, url, status=200)
        res = pinger.check_site(site)
        assert res is True


def test_check_site_exception():
    url = 'https://exception.fake.url/'
    site = {
        'url':     url,
        'timeout': 1,
    }

    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(responses.GET, url, body=Exception('Failed test'))
        res = pinger.check_site(site)
        assert res is False


def test_check_site_connect_exception():
    url = 'https://connect-exception.fake.url/'
    site = {
        'url':     url,
        'timeout': 1,
    }

    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(responses.GET, url, body=ConnectTimeout('Failed to connect'))
        res = pinger.check_site(site)
        assert res is False
