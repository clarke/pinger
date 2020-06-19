import pytest
from unittest import mock
from pinger import runner, mailer, pinger, configurator
import yaml
import os

THIS_DIR     = os.path.dirname(os.path.abspath(__file__))
TEST_CONFIG  = configurator.get_configuration(os.path.join(THIS_DIR, 'data/config.yaml'))
ACTIVE_SITES = [site for site in TEST_CONFIG['sites'] if site['enabled'] == 1]

def args_mocker(*args, **kwargs):
    class ArgsMock:
        def __init__(self, debug, dry_run, config, timeout, max_thread_workers):
            self.debug = debug
            self.dry_run = dry_run
            self.config = config
            self.max_thread_workers  = max_thread_workers
            self.timer  = timer

class ArgsMocker:
    def __init__(self, debug, dry_run, config, max_thread_workers, timer):
        self.debug   = debug
        self.dry_run = dry_run
        self.config  = config
        self.max_thread_workers  = max_thread_workers
        self.timer  = timer

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

@mock.patch('pinger.runner.check_site')
@mock.patch('concurrent.futures.ThreadPoolExecutor')
def test_check_all_sites(mock_tpe, mock_check_site):
    mock_executor = mock_tpe.executor
    mock_map = mock_executor.map
    sites = [
        {
        'url': 'http://not.a.site',
        'timeout': 0.1,
        'label': 'not.a.site',
        'email_recipients': [],
        }
    ]
    runner.check_all_sites(sites, 1)


@mock.patch('pinger.mailer.setup_email_configuration')
@mock.patch('argparse.ArgumentParser.parse_args',
            return_value=ArgsMocker(debug=False,
                                    dry_run=False,
                                    config=os.path.join(THIS_DIR, 'data/config.yaml'),
                                    max_thread_workers=1,
                                    timer=False))
@mock.patch('pinger.runner.check_all_sites')
def test_run_checks(mock_check_all_sites, mock_args_parser,
                    mock_email_configurator):
    runner.run_checks()
    mock_email_configurator.assert_called()
    mock_check_all_sites.assert_called_with(ACTIVE_SITES, 1)

@mock.patch('argparse.ArgumentParser.parse_args',
            return_value=ArgsMocker(debug=False,
                                    dry_run=False,
                                    config=os.path.join(THIS_DIR, 'data/config.yaml'),
                                    max_thread_workers=None,
                                    timer=False))
@mock.patch('pinger.runner.check_all_sites')
def test_run_checks_configged_threads(mock_check_all_sites, mock_args_parser):
    runner.run_checks()
    mock_check_all_sites.assert_called_with(ACTIVE_SITES,
                                            TEST_CONFIG['runner']['max_thread_workers'])

@mock.patch('argparse.ArgumentParser.parse_args',
            return_value=ArgsMocker(debug=False,
                                    dry_run=True,
                                    config=os.path.join(THIS_DIR, 'data/config.yaml'),
                                    max_thread_workers=1,
                                    timer=False))
@mock.patch('pinger.runner.check_all_sites')
def test_run_checks_dry_run(mock_check_all_sites, mock_args_parser):
    runner.run_checks()
    mock_check_all_sites.assert_not_called()

@mock.patch('argparse.ArgumentParser.parse_args',
            return_value=ArgsMocker(debug=True,
                                    dry_run=True,
                                    config=os.path.join(THIS_DIR, 'data/config.yaml'),
                                    max_thread_workers=1,
                                    timer=False))
@mock.patch('pinger.runner.check_all_sites')
def test_run_checks_dry_run_debug(mock_check_all_sites, mock_args_parser):
    runner.run_checks()
    mock_check_all_sites.assert_not_called()

@mock.patch('argparse.ArgumentParser.parse_args',
            return_value=ArgsMocker(debug=False,
                                    dry_run=True,
                                    config=os.path.join(THIS_DIR, 'data/config.yaml'),
                                    max_thread_workers=1,
                                    timer=True))
@mock.patch('pinger.runner.check_all_sites')
def test_run_checks_dry_run_timer(mock_check_all_sites, mock_args_parser):
    runner.run_checks()
    mock_check_all_sites.assert_not_called()

@mock.patch('argparse.ArgumentParser.parse_args',
            return_value=ArgsMocker(debug=False,
                                    dry_run=False,
                                    config=os.path.join(THIS_DIR,
                                                        'data/config-no-runner.yaml'),
                                    max_thread_workers=None,
                                    timer=True))
@mock.patch('pinger.runner.check_all_sites')
def test_run_checks_dry_run_timer(mock_check_all_sites, mock_args_parser):
    config = configurator.get_configuration(os.path.join(THIS_DIR, 'data/config-no-runner.yaml'))
    sites = [site for site in config['sites'] if site['enabled'] == 1]

    runner.run_checks()
    mock_check_all_sites.assert_called_with(sites, 5)
