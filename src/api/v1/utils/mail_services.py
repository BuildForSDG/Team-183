# third party imports
from decouple import config
# from threading import Thread

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(recipients, subject, html, msg):
    gmail_user = config('GMAIL_MAIL')  # email of sender account
    gmail_pwd = config('GMAIL_PASSWORD')  # password of sender account
    # list of email_id to send the mail
    for i in range(len(recipients)):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = gmail_user
        msg['To'] = recipients[i]

        html = html
        part2 = MIMEText(html, 'html')
        msg.attach(part2)

        s = smtplib.SMTP(config('MAIL_SERVER'), config('MAIL_PORT'))
        # s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(gmail_user, gmail_pwd)
        message = str(msg)
        # print(message)
        s.sendmail(gmail_user, recipients[i], message)
        s.quit()


def send_forgot_password_email(recipients, reset_token, url):
    """Send email with the password reset link."""
    reset_token = reset_token
    # name = name
    url = url

    reset_url = str(f'{url}?key={reset_token}')
    # reset_url = str(f'{url}?key={reset_token}&name={name}')
    subject = 'New Password Request Notification from chicken farm app'
    msg = f'Received and acknowledged request to change password. Click on the following link to reset/change your password. {reset_url}. Note that This link expires in 24hrs.'
    html = f'<html><body><p>Received and acknowledged request to change password. Click on the following link to reset/change your password.<a href={reset_url}> HERE <a/>. Note that This link expires in 24hrs.!</p></body></html>'
    send_email(recipients, subject, html, msg)


def send_confirm_reset_password_email(recipients, new_password):
    """Send email with the new reset password."""
    new_password = new_password

    subject = 'Password Reset Success Notification from chicken farm app'
    msg = f'Password Changed. Your new password is {new_password}. Use your email and password to login.'
    html = f'<html><body><p>Password Changed. Your new password is: <strong> {new_password} </strong>. Use your email and password to login!</p></body></html>'
    send_email(recipients, subject, html, msg)
