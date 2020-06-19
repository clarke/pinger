from pinger import mailer, configurator
from unittest import mock
import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

configuration_file = os.path.join(THIS_DIR, 'data/config.yaml')
configuration = configurator.get_configuration(configuration_file)
email_configuration = configuration['email']


def setup_function():
    mailer.setup_email_configuration(email_configuration)


class MockSMTP:
    def __init__(self, server, port):
        self.server = server
        self.port = port

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self

    def starttls(self, **kwargs):
        return

    def login(self, username, password):
        return

    def sendmail(self, sender, recipient, message):
        return


def test_setup_email_configuration():
    assert mailer.email_port == 587
    assert mailer.email_smtp_server == 'smtp.gmail.com'
    assert mailer.email_sender_email == 'user-account@gmail.com'
    assert mailer.email_sender_password == 'application-specific-password'


@mock.patch('smtplib.SMTP', side_effect=MockSMTP)
def test_send_email(smtp):
    message = "test message"
    recipient = "foo@bar.com"

    mailer.send_email(message, recipient)
    smtp.assert_called_with(mailer.email_smtp_server,
                            mailer.email_port)
