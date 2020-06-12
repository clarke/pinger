# Imports {{{
from pinger import pinger, mailer, configurator
import pytest
from unittest import mock
import yaml
import os
# }}}

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

def test_get_configuration():
    configuration_file = os.path.join(THIS_DIR, 'data/config.yaml')
    conf = configurator.get_configuration(configuration_file)

    assert conf['runner']['max_thread_workers'] == 8

    assert conf['email']['port']         == 587
    assert conf['email']['smtp_server']  == 'smtp.gmail.com'
    assert conf['email']['sender_email'] == 'user-account@gmail.com'
    assert conf['email']['password']     == 'application-specific-password'

    sites = [
        {
            'label': 'google',
            'email_recipients': ['user@example.com'],
            'timeout': 0.1,
            'url': 'https://google.com',
            'enabled': 1,
        },
        {
            'label': 'yahoo',
            'email_recipients': ['foo@bar.com'],
            'timeout': 1,
            'url': 'https://yahoo.com',
            'enabled': 0,
        },
    ]

    for i, site in enumerate(sites):
        for k in site.keys():
            assert conf['sites'][i][k] == sites[i][k]
