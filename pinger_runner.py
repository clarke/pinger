#!/usr/bin/env python3

# Imports {{{
import datetime
from pinger import pinger
import argparse
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
    parser.add_argument('-c', '--config', default='~/.pinger.conf',
                                          help='specify a configuration file')
    args = parser.parse_args()

    if args.debug:
        print(f"Debug: {args.debug}")
        print(f"Dry run: {args.dry_run}")
        print(f"Config: {args.config}")

    configuration = pinger.get_configuration(args.config)

    pinger.setup_email_configuration(configuration['email'])

    for site in configuration['sites'].keys():
        if args.debug:
            print(f"Processing site {site}")
        site_config = configuration['sites'][site]
        if site_config['enabled'] == 1:
            if args.debug:
                print(f"Checking site {site}")
            if not args.dry_run:
                if not pinger.check_site(site_config):
                    msg = f"""Subject: Site check failed for {site}

        Failed site check for {site}

        ---
        Timestamp: {datetime.datetime.now().isoformat()}
        URL: {site_config['url']}
        Timeout: {site_config['timeout']}
                    """
                    if args.debug:
                        print(f"Site check failed for {site}, sending alert.")
                        print(msg)
                    for email in site_config['email_recipients']:
                        if args.debug:
                            print(f"Sending alert for {site} to {email}")
                        pinger.send_email(msg, email)
        else:
            print(f"Site {site} is not enabled. Skipping.")
# }}}


# vim: foldmethod=marker foldlevel=0
