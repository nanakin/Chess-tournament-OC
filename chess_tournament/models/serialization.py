from abc import ABC, abstractmethod
from save_load_system import Register
from model import Player
from datetime import datetime


class Serializable(Register, ABC):

    @abstractmethod
    def encoder(self):
        pass

    @abstractmethod
    def decoder(self, encoded_dict):
        pass


class SerializablePlayer(Serializable, Player):
    def encoder(self):
        return {"last_name": self.last_name,
                "first_name": self.first_name,
                "birth_date": self.birth_date.strftime('%Y/%m/%d')}

    def decoder(self, encoded_dict):
        player_parameters = {"last_name": encoded_dict["last_name"],
                             "first_name": encoded_dict["first_name"],
                             "birth_date": datetime.strptime(encoded_dict["birth_date"], '%Y/%m/%d').date()}
        return Player.__init__(**player_parameters)


serializable_classes = {"Player": "SerializablePlayer"}
