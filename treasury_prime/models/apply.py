import dataclasses
import json
from treasury_prime.config import SANDBOX
import requests


@dataclasses.dataclass
class Address:
    street_line_1: str
    street_line_2: str
    city: str
    state: str
    postal_code: int


@dataclasses.dataclass
class PersonApplication:
    citizenship: str
    date_of_birth: str
    email_address: str
    first_name: str
    last_name: str
    phone_number: int
    physical_address: Address
    tin: int


def get_person_application(s: requests.Session, person_application_id: str) -> json:
    """
    Retrieve a Person Application
    https://developers.treasuryprime.com/docs/person-application#retrieve-a-person-application
    """
    person_application = s.get(SANDBOX + f'/apply/person_application/{person_application_id}')
    return person_application.json()


def get_person_applications(s: requests.Session) -> json:
    """
    List All Person Applications
    https://developers.treasuryprime.com/docs/person-application#list-all-person-applications
    """
    person_applications = s.get(SANDBOX + '/apply/person_application')
    return person_applications.json()['data']


def send_person_application(s: requests.Session, application: PersonApplication) -> json:
    data = dataclasses.asdict(application)
    person_application = s.get(SANDBOX + f'/apply/person_application', data=json.dumps(data))
    return person_application.json()['data']
