from dataclasses import dataclass


@dataclass
class Address:
    street_line_1: str
    street_line_2: str
    city: str
    state: str
    postal_code: int


@dataclass
class PersonApplication:
    citizenship: str
    date_of_birth: str
    email_address: str
    first_name: str
    last_name: str
    phone_number: int
    physical_address: Address
    tin: int
