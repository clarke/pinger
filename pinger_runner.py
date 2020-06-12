#!/usr/bin/env python3

# Imports {{{
import datetime
from pinger import pinger, mailer, configurator
import argparse
import time
import concurrent.futures
import threading
# }}}

def check_site(site): # {{{
    if args.debug:
        print(f"Checking site {site}")
    response = pinger.check_site(site)
    if response is False:
        msg = f"""Subject: Site check failed for {site['label']}

Failed site check for {site['label']}

---
Timestamp: {datetime.datetime.now().isoformat()}
URL: {site['url']}
Timeout: {site['timeout']}
        """
        if args.debug:
            print(f"Site check failed for {site['label']}, sending alert.")
            print(msg)
        for email in site['email_recipients']:
            if args.debug:
                print(f"Sending alert for {site['label']} to {email}")
            mailer.send_email(msg, email)
# }}}

def check_all_sites(sites, max_thread_workers): # {{{
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_thread_workers) as executor:
        executor.map(check_site, sites)
# }}}

if __name__ == "__main__": # {{{
    configuration_file = '~/.pinger.conf'

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-d', '--debug', default=False,
                                         action="store_true",
                                         help='turn on debug mode')
    parser.add_argument('-n', '--dry_run', default=False,
                                           action="store_true",
                                           help='show what steps would take place, but don\'t actually do them.')
    parser.add_argument('-t', '--timer', default=False,
                                           action="store_true",
                                           help='time the run')
    parser.add_argument('-c', '--config', default='~/.pinger.conf',
                                          help='specify a configuration file')
    parser.add_argument('-w', '--max_thread_workers', type=int,
                        help='Set the maximum number of worker threads')
    args = parser.parse_args()

    if args.debug:
        print(f"Debug: {args.debug}")
        print(f"Dry run: {args.dry_run}")
        print(f"Config: {args.config}")

    configuration = configurator.get_configuration(args.config)

    # Some preferential logic to set the max_thread_workers
    # Preferernce:
    # 1. Command line option
    # 2. Configuration file
    # 3. Default value (5)
    if args.max_thread_workers is not None:
        max_thread_workers = args.max_thread_workers
    elif configuration.get('runner') and configuration.get('runner').get('max_thread_workers'):
        max_thread_workers = configuration['runner']['max_thread_workers']
    else:
        max_thread_workers = 5


    if args.debug:
        print(f"Maximum thread workers: {max_thread_workers}")

    mailer.setup_email_configuration(configuration['email'])

    sites = [site for site in configuration['sites'] if site['enabled'] == 1]

    if args.debug:
        site_labels = [site['label'] for site in sites]
        print(f"Checking sites: {', '.join(site_labels)}")

        skipped_sites = [site for site in configuration['sites'] if site['enabled'] == 0]
        if len(skipped_sites) > 0:
            skipped_site_labels = [site['label'] for site in skipped_sites]
            print(f"Skipping disabled sites: {', '.join(skipped_site_labels)}")

    if args.timer:
        start_time = time.time()

    if not args.dry_run:
        check_all_sites(sites, max_thread_workers)

    if args.timer:
        duration = time.time() - start_time
        print(f"Duration: {duration} seconds")

# }}}


# vim: foldmethod=marker foldlevel=0
