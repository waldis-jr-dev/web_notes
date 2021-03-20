import smtplib
from typing import Dict
from abc import ABC, abstractmethod
from mail import mail_generator


class AbstractMail(ABC):
    @abstractmethod
    def send_verification_letter(self, recipient, link: str):
        pass

    @abstractmethod
    def send_hello_letter(self, recipient):
        pass


class Mail(AbstractMail):
    def __init__(self, sender: str, sender_password: str, smtp: str, smtp_port: str):
        self.sender = sender
        self.sender_password = sender_password
        self.smtp = smtp
        self.smtp_port = smtp_port

    def send_verification_letter(self, recipient: str, link: str):
        server = smtplib.SMTP_SSL(self.smtp, self.smtp_port)
        server.login(self.sender, self.sender_password)
        server.sendmail(self.sender,
                        recipient,
                        mail_generator.create_verification_letter(link))
        server.close()
        return {'result': True,
                'message': 'verification letter sent successfully'
                }

    def send_hello_letter(self, recipient: str):
        server = smtplib.SMTP_SSL(self.smtp, self.smtp_port)
        server.login(self.sender, self.sender_password)
        server.sendmail(self.sender,
                        recipient,
                        mail_generator.create_hello_letter(recipient.split('@')[0]))
        server.close()
        return {'result': True,
                'message': 'hello letter sent successfully'
                }


if __name__ == '__main__':
    import set_env_values
    import os

    mail = Mail(os.getenv('EMAIL_USER'), os.getenv('EMAIL_USER_PASSWORD'), os.getenv('SMTP'), os.getenv('SMTP_PORT'))

    mail.close_server()
