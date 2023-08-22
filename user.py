from flask_login import UserMixin

from db import get_session, Spender


class User(UserMixin):
    def __init__(self, id_, name, email):
        self.id = id_
        self.name = name
        self.email = email

    @staticmethod
    def get(user_id):
        session = get_session()
        spender = session.query(Spender).filter(Spender.user_id == user_id).first()
        print(spender)
        if not spender:
            return None

        spender = Spender(
            id=spender.user_id, name=spender.name, email=spender.email
        )
        return spender

    @staticmethod
    def create(id_, name, email):
        session = get_session()
        spender = Spender(name=name, email=email, user_id=id_)
        if not spender:
            return None
        session.add(spender)
        session.commit()