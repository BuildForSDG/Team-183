# third party imports
from flask_mail import Message
from decouple import config


def send_forgot_password_email(recipients, new_password):
    """Send email with new password. local import."""
    from manage import mail

    msg = Message(

        sender=config('GMAIL_MAIL'),
        recipients=recipients,
        subject='New Password Request Notification',
        body=f'Password Changed. Your new password is {new_password}.',
    )

    mail.send(msg)
