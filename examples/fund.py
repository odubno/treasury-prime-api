from treasury_prime.treasury_prime import TreasuryPrimeAPI
from treasury_prime.models import apply

r = TreasuryPrimeAPI()

# make transfer
# below are personal dummy account ids
r.book_transfer('acct_11grbtpc6e5jwm', 'acct_11grbtpc6e5jw1', 102)
r.get_balance('acct_11grbtpc6e5jwm')

# send a person application
person_application = apply.PersonApplication(
    citizenship='US',
    date_of_birth='1981-11-18',
    email_address='mikejones@who.com',
    first_name='Mike',
    last_name='Jones',
    phone_number=2813308004,
    physical_address=apply.Address(
        street_line_1='',
        street_line_2='',
        city='Houston',
        state='Texas',
        postal_code=77005,
    ),
    tin=123456789,
)
r.apply(person_application=person_application)
