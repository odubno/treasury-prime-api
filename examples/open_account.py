from treasury_prime.treasury_prime import TreasuryPrimeAPI
from treasury_prime.models.dataclass_types import account_application_type
from treasury_prime.models.dataclass_types import person_application_type

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
# TODO

# 3. Select an Account Product
account_product = r.get_account_product(account_type="checking")

# 4. Create Personal Account
person_application_id = person_application_res[0]["id"]

# {
#       "person_applications": [
#         {
#           "id": "apsn_01d5w6yaa6vt",
#           "roles": ["owner", "signer"]
#         }
#       ],
#       "primary_person_application_id": "apsn_01d5w6yaa6vt",
#       "account_product_id": "apt_11gqk87qmrax"
#     }
account_application = account_application_type.AccountApplication(
    person_applications=[
        account_application_type.PersonApplications(
            id=person_application_id,
            roles=["owner"],
        )
    ],
    primary_person_application_id=person_application_id,
    account_product_id=account_product["id"],
)

account_application_res = r.apply().create_personal_account_application(
    account_application
)
