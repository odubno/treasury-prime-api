from treasury_prime.treasury_prime import TreasuryPrimeAPI
from treasury_prime.models import apply

r = TreasuryPrimeAPI()

# make transfer
# below are personal dummy account ids
r.book_transfer("acct_11grbtpc6e5jwm", "acct_11grbtpc6e5jw1", 102)
r.get_balance("acct_11grbtpc6e5jwm")
