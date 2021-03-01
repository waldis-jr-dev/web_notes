import smtplib
from abc import ABC, abstractmethod
import mail_generator


class AbstractMail(ABC):
    @abstractmethod
    def send_verification_letter(self, recipient, link: str):
        pass

    @abstractmethod
    def send_hello_letter(self, recipient):
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

    def send_hello_letter(self, recipient: str):
        self.server.sendmail(self.__sender,
                             recipient,
                             mail_generator.create_hello_letter(recipient.split('@')[0]))

    def close_server(self):
        self.server.close()


if __name__ == '__main__':
    # for localhost (sets secret values)
    import set_env_values
    import os
    mail = Mail(os.getenv('EMAIL_USER'), os.getenv('EMAIL_USER_PASSWORD'), os.getenv('SMTP'), os.getenv('SMTP_PORT'))
    mail.send_hello_letter('grynovetskyy@gmail.com')
    mail.close_server()


