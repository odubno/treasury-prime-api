import json
from treasury_prime.config import SANDBOX
import requests


def get_person_information(s: requests.Session, person_id: str) -> json:
    person = s.get(SANDBOX + f'/person/{person_id}')
    return person.json()
