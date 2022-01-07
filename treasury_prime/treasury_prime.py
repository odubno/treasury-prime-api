import requests
from treasury_prime import config
from treasury_prime.models.book import book_transfer_request, book_transfer_is_successful
from treasury_prime.models.account import get_account


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

