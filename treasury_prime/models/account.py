import requests
import json
from treasury_prime.config import SANDBOX
from functools import lru_cache
from typing import Dict


def get_accounts(s: requests.Session) -> json:
    """
    get users' bank accounts, including balances, transactions, and owners or authorized users.
    """
    accounts = s.get(SANDBOX + "/account")
    return accounts.json()


def get_account_product(s: requests.Session, account_type: str) -> Dict:
    """
    Type of account products your organization has available
    https://developers.sandbox.treasuryprime.com/docs/account-product
    """
    if account_type not in ("checking", "savings"):
        raise Exception('account_type must be in ("checking", "savings")')
    account_products = s.get(SANDBOX + "/account_product")
    return next(
        i for i in account_products.json()["data"] if i["account_type"] == account_type
    )


@lru_cache
def get_account(s: requests.Session, account_id):
    account = s.get(SANDBOX + f"/account/{account_id}")
    return account.json()
