import re
from datetime import date


def non_empty_alphabet_validator(user_str):
    return re.match(r"^\w+((-|\s)(\w)+)*$", user_str) is not None


def date_validator(user_date_str):
    try:
        date.fromisoformat(user_date_str)
        return True
    except ValueError:
        return False


def past_date_validator(user_date_str):
    try:
        user_date = date.fromisoformat(user_date_str)
        return user_date < date.today()
    except ValueError:
        return False


def national_identifier_validator(user_id_str):
    return re.match(r"^[A-Za-z]{2}[0-9]{5}$", user_id_str) is not None