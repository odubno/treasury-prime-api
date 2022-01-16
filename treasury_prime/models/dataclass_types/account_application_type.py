from dataclasses import dataclass
from typing import List


@dataclass
class PersonApplications:
    id: str
    roles: List[str]


@dataclass
class AccountApplication:
    person_applications: List[PersonApplications]
    primary_person_application_id: str
    account_product_id: str
