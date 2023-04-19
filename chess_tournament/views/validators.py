"""Define the user input validator that can be used by the views."""
import re
from datetime import date


def non_empty_alphabet_validator(user_str: str) -> bool:
    """The string is valid if it contains word characters and optional internal spaces or dashes."""
    return re.match(r"^\w+((-|\s)(\w)+)*$", user_str) is not None


def date_validator(user_date_str: str) -> bool:
    """The string is valid if it is compatible with the ISO format (YYYY-MM-DD) and is a valid date."""
    try:
        date.fromisoformat(user_date_str)
        return True
    except ValueError:
        return False


def past_date_validator(user_date_str: str) -> bool:
    """The string is valid if it is compatible with the ISO format (YYYY-MM-DD) and is a valid past date."""
    try:
        user_date = date.fromisoformat(user_date_str)
        return user_date < date.today()
    except ValueError:
        return False


def national_identifier_validator(user_id_str: str) -> bool:
    """The string is valid if its matches 2 letters then 5 digits."""
    return re.match(r"^[A-Za-z]{2}[0-9]{5}$", user_id_str) is not None
