from abc import ABC, abstractmethod
from .requests import RequestAnswer


class IView(ABC):
    @abstractmethod
    def log(self, ok_status, to_print=None):
        pass

    @abstractmethod
    def show_log(self):
        pass

    @abstractmethod
    def show_main_menu(self) -> RequestAnswer:
        pass

    @abstractmethod
    def show_player_registration(self) -> RequestAnswer:
        pass

    @abstractmethod
    def show_tournament_registration(self) -> RequestAnswer:
        pass
