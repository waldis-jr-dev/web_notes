from abc import ABC, abstractmethod
import psycopg2
from typing import Dict, NamedTuple
import time


class User(NamedTuple):
    user_id: int
    email: str
    password: str
    role_id: int = 1
    is_active: bool = True


class Note(NamedTuple):
    note_id: int
    user_id: int
    date: int
    note: str


class AbstractPsql(ABC):
    @abstractmethod
    def add_user(self, email: str, hashed_password: str, role_id: int = 1) -> Dict[str, bool]:
        pass

    @abstractmethod
    def change_user_status(self, user_id: int, new_status: bool) -> Dict[str, bool]:
        pass

    @abstractmethod
    def change_user_role(self, user_id: int, new_role: str) -> Dict[str, bool]:
        pass

    @abstractmethod
    def change_user_password(self, user_id: int, new_password: str) -> Dict[str, bool]:
        pass

    @abstractmethod
    def add_note(self, to_user_id: int, note: str) -> Dict[str, bool]:
        pass

    @abstractmethod
    def edit_note(self, note_id: int, new_note: str) -> Dict[str, bool]:
        pass

    @abstractmethod
    def delete_note(self, note_id: int) -> Dict[str, bool]:
        pass

    @abstractmethod
    def close_connection(self) -> Dict[str, bool]:
        pass


class Psql(AbstractPsql):
    def __init__(self, psql_url: str):
        self.psql = psycopg2.connect(psql_url)
        self.cursor = self.psql.cursor()

    def add_user(self, email: str, hashed_password: str, role_id: int = 1) -> Dict[str, bool]:
        sql = f'''INSERT INTO "Users" (email, password, role_id) 
                VALUES ('{email}', '{hashed_password}', {role_id}) RETURNING user_id'''
        try:
            self.cursor.execute(sql)
        except psycopg2.errors.UniqueViolation:
            return {'result': False,
                    'message': 'user already in system'
                    }
        except Exception as e:
            raise e
        else:
            self.psql.commit()
            return {'result': True,
                    'message': 'user added successfully',
                    'user': User(self.cursor.fetchone()[0],
                                 email,
                                 hashed_password,
                                 role_id)
                    }

    def change_user_status(self, user_id: int, new_status: bool) -> Dict[str, bool]:
        sql = f'''UPDATE "Users" SET is_active = {new_status} WHERE user_id={user_id}'''
        try:
            self.cursor.execute(sql)
        # TODO
        # except psycopg2.errors:
        #     return {'result': False,
        #             'message': ''
        #             }
        except Exception as e:
            raise e
        else:
            self.psql.commit()
            return {'result': True,
                    'message': 'user status changed successfully'
                    }

    def change_user_role(self, user_id: int, new_role_id: int) -> Dict[str, bool]:
        sql = f'''UPDATE "Users" SET role_id = {new_role_id} WHERE user_id={user_id}'''
        try:
            self.cursor.execute(sql)
        # TODO
        # except psycopg2.errors:
        #     return {'result': False,
        #             'message': ''
        #             }
        except psycopg2.errors.ForeignKeyViolation:
            return {'result': False,
                    'message': 'no role with this id'
                    }
        except Exception as e:
            raise e
        else:
            self.psql.commit()
            return {'result': True,
                    'message': 'user role changed successfully'
                    }

    def change_user_password(self, user_id: int, new_password: str) -> Dict[str, bool]:
        sql = f'''UPDATE "Users" SET password = {new_password} WHERE user_id={user_id}'''
        try:
            self.cursor.execute(sql)
        # TODO
        # except psycopg2.errors:
        #     return {'result': False,
        #             'message': ''
        #             }
        except Exception as e:
            raise e
        else:
            self.psql.commit()
            return {'result': True,
                    'message': 'user password changed successfully'
                    }

    def get_user_by_email(self, email: str) -> Dict[str, bool]:
        sql = f"""SELECT user_id, email, password, role_id, is_active FROM "Users" WHERE email = '{email}'"""
        self.cursor.execute(sql)
        psql_resp = self.cursor.fetchone()
        if not psql_resp:
            return {'result': False,
                    'message': 'no user with this email'
                    }
        else:
            return {'result': True,
                    'message': 'user found successfully',
                    'user': User(psql_resp[0],
                                 psql_resp[1],
                                 psql_resp[2],
                                 psql_resp[3])
                    }

    def add_note(self, to_user_id: int, note: str) -> Dict[str, bool]:
        sql = f'''INSERT INTO "Notes" (user_id, date, note) 
                VALUES ('{to_user_id}', {int(time.time())}, '{note}') RETURNING note_id, date'''
        try:
            self.cursor.execute(sql)
        except psycopg2.errors.ForeignKeyViolation:
            return {'result': False,
                    'message': 'no user with this id'
                    }
        except Exception as e:
            raise e
        else:
            self.psql.commit()
            return {'result': True,
                    'message': 'note added successfully',
                    'note_id': Note(self.cursor.fetchone()[0],
                                    to_user_id,
                                    self.cursor.fetchone()[1],
                                    note)
                    }

    def find_notes(self, user_id: int, note_part: str = None) -> Dict[str, bool]:
        sql = f"""SELECT note_id, user_id, date, note FROM "Notes" WHERE user_id = {user_id} AND note LIKE '%{note_part}%'"""
        if not note_part:
            sql = f"""SELECT note_id, user_id, date, note FROM "Notes" WHERE user_id = {user_id}"""
        self.cursor.execute(sql)
        psql_resp = self.cursor.fetchall()
        if not psql_resp:
            return {'result': False,
                    'message': 'no notes with this parameters'
                    }
        else:
            notes = []
            for note in psql_resp:
                notes.append(Note(note[0],
                                  note[1],
                                  note[2],
                                  note[3]))

            return {'result': True,
                    'message': 'user notes found successfully',
                    'user_notes': notes
                    }

    def edit_note(self, note_id: int, new_note: str) -> Dict[str, bool]:
        sql = f'''UPDATE "Notes" SET note={new_note}, date={int(time.time())}  WHERE note_id={note_id}'''
        try:
            self.cursor.execute(sql)
        # TODO
        # except psycopg2.errors:
        #     return {'result': False,
        #             'message': ''
        #             }
        except Exception as e:
            raise e
        else:
            self.psql.commit()
            return {'result': True,
                    'message': 'note edited successfully'
                    }

    def delete_note(self, note_id: int) -> Dict[str, bool]:
        sql = f'''DELETE FROM "Notes" WHERE note_id={note_id} IF SELECT note_id from "Notes" NOT NULL'''
        try:
            self.cursor.execute(sql)
        # TODO
        # except psycopg2.errors:
        #     return {'result': False,
        #             'message': ''
        #             }
        except Exception as e:
            raise e
        else:
            self.psql.commit()
            return {'result': True,
                    'message': 'note deleted successfully'
                    }

    def close_connection(self) -> Dict[str, bool]:
        self.cursor.close()
        self.psql.close()
        return {'result': True,
                'message': 'connection closed successfully'
                }


if __name__ == '__main__':
    import set_env_values
    import os
    psql = Psql(os.getenv('DATABASE_URL'))

    print(psql.find_note(1))

    psql.close_connection()
