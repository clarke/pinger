import smtplib
import ssl

email_port = None
email_smtp_server = None
email_sender_email = None
email_sender_password = None


def setup_email_configuration(email_config):
    global email_port
    global email_smtp_server
    global email_sender_email
    global email_sender_password

    email_port = email_config['port']
    email_smtp_server = email_config['smtp_server']
    email_sender_email = email_config['sender_email']
    email_sender_password = email_config['password']


def send_email(message, recipient):
    context = ssl.create_default_context()
    with smtplib.SMTP(email_smtp_server, email_port) as server:
        server.starttls(context=context)
        server.login(email_sender_email, email_sender_password)
        server.sendmail(email_sender_email, recipient, message)
