from flask_login import UserMixin
from db import session, Doners


class Doner(UserMixin):
    def __init__(self, id_, name, email):
        self.id = id_
        self.name = name
        self.email = email

    @staticmethod
    def get(user_id):
        spender = session.query(Doners).filter(Doners.user_id == user_id).first()
        if not spender:
            return None

        return spender

    @staticmethod
    def create(id_, name, email):
        spender = Doners(name=name, email=email, user_id=id_)
        if not spender:
            return None
        session.add(spender)
        session.commit()

