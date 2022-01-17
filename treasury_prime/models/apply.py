import dataclasses
import json
from treasury_prime.config import SANDBOX
import requests
from typing import Dict
from treasury_prime.models.dataclass_types.account_application_type import (
    AccountApplication,
)
from treasury_prime.models.dataclass_types.person_application_type import (
    PersonApplication,
)


@dataclasses.dataclass
class Ach:
    # use string types to account for any leading zeros
    account_number: str
    account_type: str
    routing_number: str


@dataclasses.dataclass
class Deposit:
    # amount is double decimal; easier to define it as a string
    amount: str
    ach: Ach
    name_on_account: str


def get_person_application(s: requests.Session, person_application_id: str) -> json:
    """
    Retrieve a Person Application
    https://developers.treasuryprime.com/docs/person-application#retrieve-a-person-application
    """
    person_application = s.get(
        SANDBOX + f"/apply/person_application/{person_application_id}"
    )
    return person_application.json()


def get_person_applications(s: requests.Session) -> json:
    """
    List All Person Applications
    https://developers.treasuryprime.com/docs/person-application#list-all-person-applications
    """
    person_applications = s.get(SANDBOX + "/apply/person_application")
    return person_applications.json()["data"]


def create_person_application(s: requests.Session, data: PersonApplication) -> json:
    data = dataclasses.asdict(data)
    person_application = s.get(
        SANDBOX + f"/apply/person_application", data=json.dumps(data)
    )
    return person_application.json()["data"]


def create_personal_account_application(
    s: requests.Session, data: AccountApplication
) -> Dict:
    """
    https://developers.sandbox.treasuryprime.com/docs/account-application#create-an-account-application
    """
    data = dataclasses.asdict(data)
    account_application = s.post(
        SANDBOX + "/apply/account_application", data=json.dumps(data)
    )
    return account_application.json()


def create_deposit(s: requests.Session, data: Deposit) -> Dict:
    data = dataclasses.asdict(data)
    deposit = s.post(SANDBOX + "/apply/deposit", data=json.dumps(data))
    return deposit.json()
