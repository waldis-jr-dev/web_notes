from werkzeug.security import generate_password_hash as generate_pass_hash, \
    check_password_hash as check_pass_hash
from abc import ABC, abstractmethod


class AbstractPassCheck(ABC):
    @abstractmethod
    def generate_password_hash(self, password: str) -> str:
        pass

    @staticmethod
    @abstractmethod
    def check_password_hash(password_hash: str, password: str) -> bool:
        pass


class PassChek(AbstractPassCheck):
    def __init__(self, method: str):
        self.method = method

    def generate_password_hash(self, password: str) -> str:
        return generate_pass_hash(password, self.method)

    @staticmethod
    def check_password_hash(password_hash: str, password: str) -> bool:
        return check_pass_hash(password_hash, password)


if __name__ == '__main__':
    test = PassChek('sha256')

    print(test.generate_password_hash('qwerty'))