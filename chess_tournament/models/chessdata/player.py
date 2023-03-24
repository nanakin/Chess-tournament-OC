from dataclasses import dataclass
from datetime import date


@dataclass
class Player:
    """Player's data."""
    identifier: str
    last_name: str
    first_name: str
    birth_date: date

    def __str__(self):
        return f"{self.identifier}: {self.first_name} {self.last_name} ({self.birth_date})"