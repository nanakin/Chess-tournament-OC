"""Define the interface for the Serializable class that aims to be used on backupable chess data classes."""

from abc import ABC, abstractmethod
from typing import Any, Self


class Serializable(ABC):
    """To be backupable, the inherited class has to implement an encode and decode methods."""

    @abstractmethod
    def encode(self) -> dict:
        """Transform the instance of the object into JSON compatible format."""

    @classmethod
    @abstractmethod
    def decode(cls, encoded_dict: dict[str, Any], db: Any) -> Self:
        """Instantiate a new object from data in JSON format."""
