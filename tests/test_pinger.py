# Imports {{{
from pinger import pinger, mailer, configurator
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

# Site Check Tests {{{
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
# }}}

# Email Tests {{{
def test_setup_email_configuration():
    config = {
        'port': 123,
        'smtp_server': 'not-a-server',
        'sender_email': 'not-an-email',
        'password': 'random-password',
    }

    # Make sure they are None'd out first
    assert mailer.email_port            == None
    assert mailer.email_smtp_server     == None
    assert mailer.email_sender_email    == None
    assert mailer.email_sender_password == None

    mailer.setup_email_configuration(config)

    assert mailer.email_port            == config['port']
    assert mailer.email_smtp_server     == config['smtp_server']
    assert mailer.email_sender_email    == config['sender_email']
    assert mailer.email_sender_password == config['password']
# }}}


# vim: foldmethod=marker foldlevel=0
