import random
import string
import requests
import os
from db import session, Spender
from dotenv import load_dotenv

load_dotenv()


def new_uid():
    user_id = ""
    for i in range(4):
        user_id += ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
        if i != 3:
            user_id += "-"

    while True:
        spender_id = session.query(Spender).filter(Spender.user_id == user_id).first()
        if not spender_id:
            break

    return user_id


def check_spender(mail):
    spender = session.query(Spender).filter(Spender.email == mail).first()
    if spender:
        return spender.user_id

    if not spender:
        return None


def get_iserv_provider_cfg():
    return requests.get(os.getenv("ISERV_DISCORVERY_URL")).json()
