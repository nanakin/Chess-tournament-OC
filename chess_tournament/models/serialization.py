from abc import ABC, abstractmethod


class Serializable(ABC):
    @abstractmethod
    def encode(self):
        pass

    @classmethod
    def decode(cls, encoded_dict):
        pass
