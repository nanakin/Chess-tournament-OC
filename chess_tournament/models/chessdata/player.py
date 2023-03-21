from dataclasses import dataclass
from datetime import date


@dataclass
class Player:
    """Player's data."""
    id: str
    last_name: str
    first_name: str
    birth_date: date
