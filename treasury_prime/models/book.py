import requests
import time
import json
from treasury_prime.config import SANDBOX


def book_transfer_is_successful(s: requests.Session, book_transfer_id: str) -> bool:
    # This should be a webhook
    # https://developers.sandbox.treasuryprime.com/guides/book-transfers#3-get-status-updates
    is_successful = False
    attempts = 0
    while is_successful is False:
        # wait 1 second before checking again
        time.sleep(1)
        if attempts == 10:
            return False
        book_body = transfer_id_request(s, book_transfer_id)
        if book_body['status'] == 'sent':
            print(f'book_transfer_is_successful after {attempts} attempts')
            return True
        attempts += 1


def transfer_id_request(s: requests.Session, book_transfer_id: str) -> json:
    book_response = s.get(SANDBOX + f'/book/{book_transfer_id}')
    book_response.raise_for_status()
    return book_response.json()


def book_transfer_request(s: requests.Session, from_account_id: str, to_account_id: str, amount: float) -> json:
    book_response = s.post(SANDBOX + '/book', data=json.dumps({
        'amount': "{:.2f}".format(amount),  # needs to be a string and rounded to 2 decimal places
        'from_account_id': from_account_id,
        'to_account_id': to_account_id,
    }))
    book_response.raise_for_status()
    return book_response.json()
