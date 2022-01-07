from treasury_prime.treasury_prime import TreasuryPrimeAPI
from mock import patch, Mock
import pytest


def mock_book_transfer_request():
    return Mock(return_value={
        'to_account_id': 'acct_1',
        'description': None,
        'amount': '100.00',
        'bankdata': None,
        'bank_id': 'bank_treasuryprime',
        'from_account_id': 'acct_2',
        'org_id': 'org_1',
        'updated_at': '2022-01-07T00:42:28Z',
        'status': 'pending',
        'id': 'book_1',
        'error': None,
        'created_at': '2022-01-07T00:42:28Z',
        'userdata': None
    })


def mock_transfer_id_request():
    return Mock(return_value={
        'to_account_id': 'acct_1',
        'description': None,
        'amount': '100.00',
        'bankdata': None,
        'bank_id': 'bank_treasuryprime',
        'from_account_id': 'acct_1',
        'org_id': 'org_1',
        'updated_at': '2022-01-07T00:42:28Z',
        'status': 'sent',
        'id': 'book_1',
        'error': None,
        'created_at': '2022-01-07T00:42:28Z',
        'userdata': None
    })


def mock_get_account_low_available_balance():
    return Mock(return_value={'address': {'street_line_1': '215 Kearny St', 'street_line_2': None, 'city': 'San Francisco', 'state': 'CA', 'postal_code': '94102'}, 'account_type': 'savings', 'bank_id': 'bank_treasuryprime', 'person_ids': ['psn_11grbtpc6e5jwp'], 'available_balance': '1.00', 'name': 'oleh dubno', 'org_id': 'org_1fkshrk60m4', 'updated_at': '2022-01-07T04:00:23Z', 'currency': 'USD', 'routing_number': '000000000', 'status': 'open', 'primary_person_id': 'psn_11grbtpc6e5jwp', 'account_number': '137000477144', 'locked': False, 'id': 'acct_1', 'funded': True, 'business_ids': [], 'current_balance': '1.00', 'created_at': '2021-11-06T02:39:08Z', 'lock': None, 'userdata': None})


def mock_get_account_high_available_balance():
    return Mock(return_value={'address': {'street_line_1': '215 Kearny St', 'street_line_2': None, 'city': 'San Francisco', 'state': 'CA', 'postal_code': '94102'}, 'account_type': 'savings', 'bank_id': 'bank_treasuryprime', 'person_ids': ['psn_11grbtpc6e5jwp'], 'available_balance': '5000.00', 'name': 'oleh dubno', 'org_id': 'org_1fkshrk60m4', 'updated_at': '2022-01-07T04:00:23Z', 'currency': 'USD', 'routing_number': '000000000', 'status': 'open', 'primary_person_id': 'psn_11grbtpc6e5jwp', 'account_number': '137000477144', 'locked': False, 'id': 'acct_1', 'funded': True, 'business_ids': [], 'current_balance': '5000.00', 'created_at': '2021-11-06T02:39:08Z', 'lock': None, 'userdata': None})


@patch('treasury_prime.models.book.transfer_id_request', mock_transfer_id_request())
@patch('treasury_prime.treasury_prime.book_transfer_request', mock_book_transfer_request())
@patch('treasury_prime.treasury_prime.get_account', mock_get_account_high_available_balance())
def test_book_transfer_is_successful():
    tp = TreasuryPrimeAPI()
    tp.book_transfer('acct_1', 'acct_2', 100)


@patch('treasury_prime.models.book.transfer_id_request', mock_transfer_id_request())
@patch('treasury_prime.treasury_prime.book_transfer_request', mock_book_transfer_request())
@patch('treasury_prime.treasury_prime.get_account', mock_get_account_low_available_balance())
def test_book_transfer_insufficient_funds():
    tp = TreasuryPrimeAPI()
    with pytest.raises(Exception, match="Sender account has insufficient funds"):
        tp.book_transfer('acct_1', 'acct_2', 100)
