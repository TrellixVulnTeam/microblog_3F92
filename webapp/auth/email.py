from flask_mail import Message
from webapp import mail

from flask import render_template
from threading import Thread
from flask import current_app


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    #mail.send(msg)
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('Réinitialiser votre mot de passe', sender=current_app.config['MAIL_USERNAME'],
               recipients=[user.email], text_body=render_template('email/reset_password.txt',
                user=user, token=token), html_body=render_template('email/reset_password_request.html',
                 user=user, token=token))
