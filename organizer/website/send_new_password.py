from random import choice
import random
import string
import smtplib
from website.sending_settings import SENDER_EMAIL, SENDER_PASSWORD, SERVER, PORT


def generate_new_password():
    length = random.randint(8, 10)
    chars = string.ascii_letters + string.digits
    return ''.join([choice(chars) for i in range(length)])


def send_reset_password(receiver, new_password):
    TO = receiver
    SUBJECT = "New password"
    TEXT = "Your new passowrd is  {}".format(new_password)
    message = 'Subject: %s\n\n%s' % (SUBJECT, TEXT)
    server = smtplib.SMTP(SERVER, PORT)
    server.ehlo()
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, [TO], message)


def send_feedback(receiver, text, name, email):
    TO = receiver
    SUBJECT = "Contact form email from " + name
    TEXT = text + "\n Send from " + email
    message = 'Subject: %s\n\n%s' % (SUBJECT, TEXT)
    server = smtplib.SMTP(SERVER, PORT)
    server.ehlo()
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, [TO], message)
