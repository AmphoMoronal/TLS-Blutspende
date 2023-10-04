from flask import current_app, g
import os
from sqlalchemy import create_engine, Column, Integer, BigInteger, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

engine = create_engine("sqlite:///test.db")

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Doners(Base):
    __tablename__ = "doners"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String, unique=True)
    user_id = Column(String, unique=True)
    is_authenticated = Column(Boolean, default=True)
    appointment = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"Doners(id={self.id!r}, name={self.name!r}, email={self.email!r}, user_id={self.user_id!r}," \
               f" is_authenticated={self.is_authenticated!r}, appointment={self.appointment!r}, " \
               f"admin={self.admin})"


class Appointments(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True)
    date = Column(String(10))
    time = Column(String(4))
    left_slots = Column(Integer, default=4)
    doner1 = Column(String(50), unique=True)
    doner2 = Column(String(50), unique=True)
    doner3 = Column(String(50), unique=True)
    doner4 = Column(String(50), unique=True)

    def __repr__(self) -> str:
        return f"Appointments(date={self.date!r}, time={self.time!r}," \
               f"left_slots={self.left_slots!r}," \
               f"doner1={self.doner1!r}, doner2={self.doner2!r}," \
               f"doner3={self.doner3!r}, doner4={self.doner4!r})"


Base.metadata.create_all(engine)
