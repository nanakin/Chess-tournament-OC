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
        return f"player {self.identifier}: {self.last_name} {self.first_name} ({self.birth_date})"

    def __lt__(self, other):
        return self.last_name.upper() < other.last_name.upper()
