from abc import ABC, abstractmethod


class Serializable(ABC):

    @abstractmethod
    def encode(self):
        pass

    @abstractmethod
    def decode(self, encoded_dict):
        pass
