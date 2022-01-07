import requests
import json
from treasury_prime.config import SANDBOX
from functools import lru_cache


def get_accounts(s: requests.Session) -> json:
    """
    get users' bank accounts, including balances, transactions, and owners or authorized users.
    """
    accounts = s.get(SANDBOX + '/account')
    return accounts.json()


@lru_cache
def get_account(s: requests.Session, account_id):
    account = s.get(SANDBOX + f'/account/{account_id}')
    return account.json()
