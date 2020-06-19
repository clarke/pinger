import pytest
from unittest import mock
from pinger import runner, mailer, pinger

def args_mocker(*args, **kwargs):
    class ArgsMock:
        def __init__(self, debug, verbose, dry_run):
            self.debug = debug
            self.verbose = verbose
            self.dry_run = dry_run


@mock.patch('pinger.runner.args', side_effect=args_mocker)
@mock.patch('pinger.pinger.check_site', return_value=True)
@mock.patch('pinger.mailer.send_email')
def test_check_site_success(mock_send_email, mock_check_site, mock_args):
    mock_args.debug   = True
    mock_args.verbose = False
    mock_args.dry_run = False

    site = {
        'url': 'http://not.a.site',
        'timeout': 0.1,
        'label': 'not.a.site',
        'email_recipients': [],
    }
    runner.check_site(site)
    mock_check_site.assert_called_with(site)
    mock_send_email.assert_not_called()

@mock.patch('pinger.runner.args', side_effect=args_mocker)
@mock.patch('pinger.pinger.check_site', return_value=False)
@mock.patch('pinger.mailer.send_email')
def test_check_site_failed(mock_send_email, mock_check_site, mock_args):
    mock_args.debug   = True
    mock_args.verbose = False
    mock_args.dry_run = False

    site = {
        'url': 'http://not.a.site',
        'timeout': 0.1,
        'label': 'not.a.site',
        'email_recipients': ['nobody'],
    }
    runner.check_site(site)
    mock_check_site.assert_called_with(site)
    mock_send_email.assert_called()
