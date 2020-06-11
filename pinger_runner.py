#!/usr/bin/env python3

# Imports {{{
import datetime
from pinger import pinger
# }}}


if __name__ == "__main__": # {{{
    configuration_file = '~/.pinger.conf'
    configuration = pinger.get_configuration(configuration_file)

    pinger.setup_email_configuration(configuration['email'])

    for site in configuration['sites'].keys():
        site_config = configuration['sites'][site]
        if site_config['enabled'] == 1:
            if not pinger.check_site(site_config):
                msg = f"""Subject: Site check failed for {site}

    Failed site check for {site}

    ---
    Timestamp: {datetime.datetime.now().isoformat()}
    URL: {site_config['url']}
    Timeout: {site_config['timeout']}
                """
                for email in site_config['email_recipients']:
                    pinger.send_email(msg, email)
# }}}


# vim: foldmethod=marker foldlevel=0
