from abc import ABC, abstractmethod
import psycopg2
from typing import Union
import time


class AbstractPsql(ABC):
    @abstractmethod
    def add_user(self, email: str, hashed_password: str, role_id: int = 1) -> int:
        pass

    @abstractmethod
    def add_note(self, to_user_id: int, note: str) -> Union[str, int]:
        pass


class Psql(AbstractPsql):
    def __init__(self, psql_url: str):
        self.psql = psycopg2.connect(psql_url)
        self.cursor = self.psql.cursor()

    def add_user(self, email: str, hashed_password: str, role_id: int = 1) -> Union[str, int]:
        sql = f'''INSERT INTO "Users" (email, password, role_id) 
                VALUES ('{email}', '{hashed_password}', {role_id}) RETURNING user_id'''
        try:
            self.cursor.execute(sql)
        except psycopg2.errors.UniqueViolation:
            return 'user already in system'
        except Exception as e:
            raise e
        else:
            self.psql.commit()
            return self.cursor.fetchone()[0]

    def add_note(self, to_user_id: int, note: str) -> Union[str, int]:
        sql = f'''INSERT INTO "Notes" (user_id, date, note) 
                VALUES ('{to_user_id}', {int(time.time())}, '{note}') RETURNING note_id'''
        try:
            self.cursor.execute(sql)
        except psycopg2.errors.ForeignKeyViolation:
            return 'no user with this id'
        except Exception as e:
            raise e
        else:
            self.psql.commit()
            return self.cursor.fetchone()[0]


if __name__ == '__main__':
    import set_env_values
    import os
    psql = Psql(os.getenv('DATABASE_URL'))
    print(psql.add_note(2, 'test_note'))
