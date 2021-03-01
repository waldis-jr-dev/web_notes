from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def create_verification_letter(link: str):
    msg = MIMEMultipart('alternative')

    msg['Subject'] = "Web Notes email verification."

    with open('verification_letter.html', 'r') as verification_letter_as_html:
        msg.attach(MIMEText(verification_letter_as_html.read().format(verification_link=link), 'html'))

    return msg.as_string()


def create_hello_letter(user: str):
    msg = MIMEMultipart('alternative')

    msg['Subject'] = "Web Notes."

    with open('hello_letter.html', 'r') as hello_letter_as_html:
        msg.attach(MIMEText(hello_letter_as_html.read().format(user=user), 'html'))
    return msg.as_string()
