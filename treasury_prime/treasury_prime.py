import requests
from treasury_prime import config
from treasury_prime.models.book import book_transfer_request, book_transfer_is_successful
from treasury_prime.models.account import get_account
from treasury_prime.models.apply import send_person_application, PersonApplication


class TreasuryPrimeAPI(object):

    def __init__(self):
        self._session = requests.Session()
        self._session.auth = (config.KEY_ID, config.SECRET_KEY)
        self._session.headers = {
            'Content-Type': 'application/json'
        }

    def get_balance(self, account_id) -> float:
        account = get_account(self._session, account_id)
        return float(account['available_balance'])

    def book_transfer(self, from_account_id: str, to_account_id: str, amount: float) -> bool:
        """
        A book transfer is an electronic funds transfer between two accounts at the same bank
        """
        # confirm account that's sending money has sufficient funds
        if self.get_balance(from_account_id) < amount:
            raise Exception('Sender account has insufficient funds')

        # transfer money
        book_body = book_transfer_request(self._session, from_account_id, to_account_id, amount)

        # verify transfer is successful
        if not book_transfer_is_successful(self._session, book_body['id']):
            raise Exception('Book Transfer is still in pending')
        return True

    def apply(self, person_application: PersonApplication = None, business: bool = False):
        """
        Apply to open a new bank account, or apply to add additional authorized users to an existing account
        Send emails for application approval/denial
        https://developers.treasuryprime.com/docs/apply
        """
        if person_application:
            person_application_res = send_person_application(self._session, person_application)
            return person_application_res
        elif business:
            pass
        else:
            raise Exception("apply must include an arg for either person or business")

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

