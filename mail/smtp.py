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

    @abstractmethod
    def close_server(self) -> Dict[str, bool]:
        pass


class Mail(AbstractMail):
    def __init__(self, sender: str, sender_password: str, smtp: str, smtp_port: str):
        self.__sender = sender
        self.server = smtplib.SMTP_SSL(smtp, smtp_port)
        self.server.login(sender, sender_password)

    def send_verification_letter(self, recipient: str, link: str):
        self.server.sendmail(self.__sender,
                             recipient,
                             mail_generator.create_verification_letter(link))
        return {'result': True,
                'message': 'verification letter sent successfully'
                }

    def send_hello_letter(self, recipient: str):
        self.server.sendmail(self.__sender,
                             recipient,
                             mail_generator.create_hello_letter(recipient.split('@')[0]))
        return {'result': True,
                'message': 'hello letter sent successfully'
                }

    def close_server(self) -> Dict[str, bool]:
        self.server.close()
        return {'result': True,
                'message': 'connection closed successfully'
                }


if __name__ == '__main__':
    import set_env_values
    import os
    mail = Mail(os.getenv('EMAIL_USER'), os.getenv('EMAIL_USER_PASSWORD'), os.getenv('SMTP'), os.getenv('SMTP_PORT'))

    mail.close_server()


