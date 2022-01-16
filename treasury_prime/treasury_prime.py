import requests
from typing import List
from treasury_prime import config
from treasury_prime.models.book import (
    book_transfer_request,
    book_transfer_is_successful,
)
from treasury_prime.models.account import get_account, get_account_product
from treasury_prime.models.person import get_person_information
from treasury_prime.models.apply import (
    create_person_application,
    create_personal_account_application,
)
from treasury_prime.models.dataclass_types.person_application_type import (
    PersonApplication,
)
from treasury_prime.models.dataclass_types.account_application_type import (
    AccountApplication,
)


class TreasuryPrimeAPI(object):
    def __init__(self):
        self._session = requests.Session()
        self._session.auth = (config.KEY_ID, config.SECRET_KEY)
        self._session.headers = {"Content-Type": "application/json"}

    def get_person_information(self, person_id: str):
        return get_person_information(self._session, person_id)

    def get_balance(self, account_id) -> float:
        account = get_account(self._session, account_id)
        return float(account["available_balance"])

    def book_transfer(
        self, from_account_id: str, to_account_id: str, amount: float
    ) -> bool:
        """
        A book transfer is an electronic funds transfer between two accounts at the same bank
        """
        # confirm account that's sending money has sufficient funds
        if self.get_balance(from_account_id) < amount:
            raise Exception("Sender account has insufficient funds")

        # transfer money
        book_body = book_transfer_request(
            self._session, from_account_id, to_account_id, amount
        )

        # verify transfer is successful
        if not book_transfer_is_successful(self._session, book_body["id"]):
            raise Exception("Book Transfer is still in pending")
        return True

    def ach_transfer(self):
        """
        An Automated Clearing House (ACH) transfer is an electronic funds transfer between two accounts at different banks.
        """
        pass

    def issue_card(self):
        """
        Issue debit cards.
        """
        pass

    def add_authorized_user(self):
        # https://developers.sandbox.treasuryprime.com/guides/authorized-users
        pass

    def get_account_product(self, account_type: str):
        return get_account_product(self._session, account_type)

    def apply(self):
        # pass existing session to _Apply object
        return _Apply(self._session)


class _Apply:

    """
    _Apply is a local class object to carry out functionality around adding a new bank account
    or apply to add additional authorized users to an existing account
    Send emails for application approval/denial
    https://developers.treasuryprime.com/docs/apply
    """

    def __init__(self, _session):
        self._session = _session

    def person_application(self, data: PersonApplication) -> List:
        """ """
        return create_person_application(self._session, data)

    def business_application(self):
        pass

    def additional_person_application(self):
        """
        Add additional people to an account that has already been opened by
        associating a person_application_id with an account_id
        https://developers.treasuryprime.com/docs/additional-person-application
        """
        pass

    def create_personal_account_application(self, data: AccountApplication):
        """
        Create an application for a new bank account
        https://developers.treasuryprime.com/docs/account-application#create-an-account-application
        """
        return create_personal_account_application(self._session, data)
