# Imports {{{
import pinger
import pytest
from unittest import mock
import re, datetime, os
import requests
import responses
import yaml
from requests.exceptions import ConnectTimeout
# }}}

# Setup and teardown {{{
def setup_function():
    pass

def teardown_function():
    # Set the global variables back to default values
    pinger.email_port            = None
    pinger.email_smtp_server     = None
    pinger.email_sender_email    = None
    pinger.email_sender_password = None

# }}}

# Tests {{{
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

        res = pinger.check_site(site)
        assert res == False


def test_check_site_connect_exception():
    url = 'https://connect-exception.fake.url/'
    site = {
        'url':     url,
        'timeout': 1,
    }

    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(responses.GET, url, body=ConnectTimeout('Failed to connect'))

        res = pinger.check_site(site)
        assert res == False


def test_setup_email_configuration():
    config = {
        'port': 123,
        'smtp_server': 'not-a-server',
        'sender_email': 'not-an-email',
        'password': 'random-password',
    }

    # Make sure they are None'd out first
    assert pinger.email_port            == None
    assert pinger.email_smtp_server     == None
    assert pinger.email_sender_email    == None
    assert pinger.email_sender_password == None

    pinger.setup_email_configuration(config)

    assert pinger.email_port == config['port']
    assert pinger.email_smtp_server == config['smtp_server']
    assert pinger.email_sender_email == config['sender_email']
    assert pinger.email_sender_password == config['password']



# }}}


# vim: foldmethod=marker foldlevel=0
