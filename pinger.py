#!/usr/bin/env python3

# Imports {{{
import requests
import yaml
from pathlib import Path
import os
import smtplib, ssl
import datetime
# }}}

# Configuration {{{
configuration_file = '~/.pinger.conf'
email_port = None
email_smtp_server = None
email_sender_email = None
email_sender_password = None
# }}}

# Custom Exceptions {{{
class StatusCodeException(Exception):
    pass
# }}}

def get_configuration():
    with open(Path(os.path.expanduser('~/.pinger.conf'))) as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)
    return conf

def setup_email_configuration(email_config):
    global email_port
    global email_smtp_server
    global email_sender_email
    global email_sender_password

    email_port            = email_config['port']
    email_smtp_server     = email_config['smtp_server']
    email_sender_email    = email_config['sender_email']
    email_sender_password = email_config['password']


def check_site(site):
    try:
        res = requests.get(site['url'], timeout=site['timeout'])
        if res.status_code != 200:
            print(f"Status code: {res.status_code}")
            return False
        return True
    except requests.exceptions.ConnectTimeout as cte:
        print(f"Connection timeout for {site['url']}")
    except Exception as e:
        print(f"Exception occurred: {e}")
        return False

def send_email(message, recipient):
	context = ssl.create_default_context()
	with smtplib.SMTP(email_smtp_server, email_port) as server:
		server.starttls(context=context)
		server.login(email_sender_email, email_sender_password)
		server.sendmail(email_sender_email, recipient, message)

if __name__ == "__main__": # {{{
    configuration = get_configuration()

    setup_email_configuration(configuration['email'])

    for site in configuration['sites'].keys():
        site_config = configuration['sites'][site]
        if site_config['enabled'] == 1:
            if not check_site(site_config):
                msg = f"""Subject: Site check failed for {site}

    Failed site check for {site}

    ---
    Timestamp: {datetime.datetime.now().isoformat()}
    URL: {site_config['url']}
    Timeout: {site_config['timeout']}
                """
                for email in site_config['email_recipients']:
                    send_email(msg, email)
            else:
                # print(f"Successful check for {site}")
                pass
# }}}

# vim: foldmethod=marker foldlevel=0
