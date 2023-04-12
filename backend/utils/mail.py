import smtplib
from email.message import EmailMessage


def send_mail(password, to):
    host = 'smtp.gmail.com'
    port = 465
    server = smtplib.SMTP_SSL(host=host, port=port)
    server.login('hoangxuanlong4@gmail.com', 'dcwvsoeyfrhkuhfs')
    content = f'this is new pass: {password}'

    try:
        msg = EmailMessage()
        msg.set_content(content)
        msg["From"] = 'hoangxuanlong4@gmail.com'
        msg["To"] = to
        msg['ReturnPath'] = 'hoangxuanlong4@gmail.com'
        # msg["To"] = 'bangtx@otani-trading.com'
        msg["Subject"] = 'reset password'

        server.send_message(msg)

    except smtplib.SMTPResponseException as e:
        error_message = e.smtp_error
