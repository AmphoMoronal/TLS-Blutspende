from flask import current_app, g
import os
from sqlalchemy import create_engine, Column, Integer, BigInteger, String, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(
    f'postgresql://{os.getenv("PSQL_USER")}:{os.getenv("PSQL_PASSWORD")}@{os.getenv("PSQL_HOST")}/{os.getenv("PSQL_TABLE")}',
    echo=True)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Spender(Base):
    __tablename__ = "spender"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String, unique=True)
    user_id = Column(String, unique=True)
    is_authenticated = Column(Boolean, default=True)
    volljaehrig = Column(Boolean)

    def __repr__(self) -> str:
        return f"Spender(id={self.user_id!r}, name={self.name!r}, email={self.email!r}, user_id={self.user_id}," \
               f" volljaehrig={self.volljaehrig}, is_authenticated={self.is_authenticated})"


class Termine(Base):
    __tablename__ = "termine"
    time = Column(String(5), primary_key=True)
    spender = Column(String(50))
    spender_mail = Column(String(50))

    def __repr__(self) -> str:
        return f"Termine(zeit={self.time!r}, spender={self.spender!r}), spender_mail={self.spender_mail!r}"

Base.metadata.create_all(engine)


def get_session():
    if "session" not in g:
        g.session = session

    return g.session


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
