"""Define players related data structures."""

from dataclasses import dataclass
from datetime import date
from typing import Any, Optional, Self

from ..serialization import Serializable


@dataclass
class Player(Serializable):
    """Player's data."""

    identifier: str
    last_name: str
    first_name: str
    birth_date: date

    def __str__(self) -> str:
        """return string representation of a player instance."""
        return f"{self.last_name} {self.first_name} ({self.identifier})"

    def __lt__(self, other: Self) -> bool:
        """Order players by last name."""
        return self.last_name.upper() < other.last_name.upper()

    def encode(self) -> dict[str, Any]:
        """Transform the instance of the object into JSON compatible format."""
        return {
            "identifier": self.identifier,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birth_date": str(self.birth_date),
        }

    @classmethod
    def decode(cls, encoded_data: dict[str, Any], db: Optional[dict | list] = None) -> Self:
        """Instantiate a new object from data in JSON format."""
        encoded_data["birth_date"] = date.fromisoformat(encoded_data["birth_date"])
        return cls(**encoded_data)
