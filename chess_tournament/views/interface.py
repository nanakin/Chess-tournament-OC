"""Define the interface for all the views classes, these methods will be used by the controller."""
from abc import ABC, abstractmethod
from .requests import RequestAnswer


class IView(ABC):
    """A "valid" view must implements the following methods."""

    @abstractmethod
    def log(self, ok_status, to_print=None):
        """Add a log to the log queue."""

    @abstractmethod
    def show_log(self):
        """Display logs and purge the queue."""

    @abstractmethod
    def show_main_menu(self) -> RequestAnswer:
        """Display the main select menu."""

    @abstractmethod
    def show_player_registration(self) -> RequestAnswer:
        """Ask for player’s first/last name, birthdate and ID."""

    @abstractmethod
    def show_tournament_registration(self) -> RequestAnswer:
        """Ask for tournament name, location, dates and rounds number."""
