# Imports {{{
import pinger
import pytest
from unittest import mock
import re, datetime, os
import requests
import responses
# }}}

def test_check_site_not_found():
    url = 'https://fake.url/'

    site = {
        'url':     url,
        'timeout': 1,
    }

    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(responses.GET, url, status=404)

        res = pinger.check_site(site)

        assert res == False
        assert len(rsps.calls) == 1
        assert rsps.calls[0].request.url == url
        assert rsps.calls[0].response.status_code == 404


def test_check_site_success():
    url = 'https://fake.url/'
    site = {
        'url':     url,
        'timeout': 1,
    }

    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(responses.GET, url, status=200)

        res = pinger.check_site(site)

        assert res == True
        assert len(rsps.calls) == 1
        assert rsps.calls[0].request.url == url
        assert rsps.calls[0].response.status_code == 200


def test_check_site_exception():
    url = 'https://exception.fake.url/'
    site = {
        'url':     url,
        'timeout': 1,
    }

    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(responses.GET, url, body=Exception('Failed test'))

        with pytest.raises(Exception):
            pinger.check_site(site)


def test_check_site_connect_exception():
    url = 'https://connect-exception.fake.url/'
    site = {
        'url':     url,
        'timeout': 1,
    }

    ex = requests.exceptions.ConnectTimeout

    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(responses.GET,
                 url,
                 body=ex('Failed to connect'))

        with pytest.raises(ex):
            pinger.check_site(site)

# vim: foldmethod=marker foldlevel=0
