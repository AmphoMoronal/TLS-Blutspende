from flask import current_app, g
import os
from sqlalchemy import create_engine, Column, Integer, BigInteger, String, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

engine = create_engine("sqlite:///test.db")

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
    first_time = Column(Boolean, default=False)
    adult = Column(Boolean, default=False)
    weight = Column(Boolean, default=False)
    healthy = Column(Boolean, default=False)
    tattoos = Column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"Spender(id={self.user_id!r}, name={self.name!r}, email={self.email!r}, user_id={self.user_id}," \
               f" adult={self.adult}, is_authenticated={self.is_authenticated})"


class Appointments(Base):
    __tablename__ = "termine"
    id = Column(Integer, primary_key=True)
    date = Column(String(10))
    time = Column(String(4))
    left_slots = Column(Integer, default=4)
    spender1 = Column(String(50))
    spender1_mail = Column(String(50))
    spender2 = Column(String(50))
    spender2_mail = Column(String(50))
    spender3 = Column(String(50))
    spender3_mail = Column(String(50))
    spender4 = Column(String(50))
    spender4_mail = Column(String(50))

    def __repr__(self) -> str:
        return (f"Appointments(date={self.date!r}, time={self.time!r},"
                f"left_slots={self.left_slots!r}"
                f"spender1={self.spender!r}), spender1_mail={self.spender_mail!r},"
                f"spender2={self.spender2!r}, spender2_mail={self.spender2_mail!r},"
                f"spender3={self.spender3!r}, spender3_mail={self.spender3_mail!r},"
                f"spender4={self.spender4!r}, spender4_mail={self.spender4_mail!r}")

Base.metadata.create_all(engine)
