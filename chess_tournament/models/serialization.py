"""Define the interface for the Serializable class that aims to be used on backupable chess data classes."""

from abc import ABC, abstractmethod


class Serializable(ABC):
    """To be backupable, the inherited class has to implement an encode and decode methods."""

    @abstractmethod
    def encode(self):
        """Transform the instance of the object into JSON compatible format."""

    @classmethod
    def decode(cls, encoded_dict, *db):
        """Instantiate a new object from data in JSON format."""
