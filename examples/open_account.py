from treasury_prime.treasury_prime import TreasuryPrimeAPI
from treasury_prime.models.dataclass_types import account_application_type
from treasury_prime.models.dataclass_types import person_application_type
from treasury_prime.models.apply import Deposit, Ach


r = TreasuryPrimeAPI()

"""
https://developers.sandbox.treasuryprime.com/guides/open-accounts
"""

# Define dummy input data
person_application = person_application_type.PersonApplication(
    citizenship="US",
    date_of_birth="1981-11-18",
    email_address="mikejones@who.com",
    first_name="Mike",
    last_name="Jones",
    phone_number=2813308004,
    physical_address=person_application_type.Address(
        street_line_1="",
        street_line_2="",
        city="Houston",
        state="Texas",
        postal_code=77005,
    ),
    # tin beginning with 1 will automatically approve application
    # https://developers.treasuryprime.com/docs/apply-testing#personal-applications
    tin=123456789,
)

# 1. Create a Person Application
# send a person application
person_application_res = r.apply().person_application(data=person_application)

# 2. Create a deposit (optional)
deposit_req = Deposit(
    amount="100.00",
    ach=Ach(
        account_number="137000477122",
        account_type="checking",
        routing_number="011000015",
    ),
    name_on_account="Oleh Dubno",
)
deposit = r.apply().create_deposit(deposit_req)

# 3. Select an Account Product
account_product = r.get_account_product(
    account_type="checking", ownership_type="personal"
)


# 4. Create Personal Account
# application res is a list with a single item atm
person_application_id = person_application_res[0]["id"]

# it seems that personal accounts cannot be created without having a business
# the error response when creating an application should be explicit as to whether the application is for a business or personal
account_application = account_application_type.AccountApplication(
    person_applications=[
        account_application_type.PersonApplications(
            id=person_application_id,
            # where do I find roles for a person?
            roles=["owner"],
        )
    ],
    primary_person_application_id=person_application_id,
    account_product_id=account_product["id"],
)
account_application_res = r.apply().create_personal_account_application(
    account_application
)
