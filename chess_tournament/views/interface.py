"""Define the interface for all the views classes, these methods will be used by the controller."""
from abc import ABC, abstractmethod
from typing import Any, Optional

from .requests import RequestAnswer


class IView(ABC):
    """A "valid" view must implements the following methods."""

    # --- common methods ---

    @abstractmethod
    def log(self, ok_status: bool, to_print: Optional[str] = None):
        """Add a log to the log queue."""

    @abstractmethod
    def show_log(self):
        """Display logs and purge the queue."""

    @abstractmethod
    def show_confirmation(self, to_confirm: str) -> RequestAnswer:
        """Display a yes/no question."""

    @abstractmethod
    def ask_saving_path(self) -> RequestAnswer:
        """Display an autocomplete path input."""

    @abstractmethod
    def show_list_menu(self, total: int, data_name: str) -> RequestAnswer:
        """Display a menu to print or export a list."""

    @abstractmethod
    def print_list(self, data_name: str, info_list: list[str]) -> RequestAnswer:
        """Display the given list then suggest to export it."""

    # --- main menu method ---

    @abstractmethod
    def show_main_menu(self) -> RequestAnswer:
        """Display the main menu."""

    # --- matches methods ---

    @abstractmethod
    def select_match(self, matches_info: list[str]) -> RequestAnswer:
        """Display a menu with the round’s matches list."""

    @abstractmethod
    def enter_score(self, players: tuple[str, str]) -> RequestAnswer:
        """Display a menu to select the participants score (WIN/LOSE/DRAW)."""

    # --- participants methods ---

    @abstractmethod
    def show_manage_participants_menu(self, total_participants: int) -> RequestAnswer:
        """Display a menu to manage participants."""

    # --- players methods ---

    @abstractmethod
    def show_manage_player_menu(self) -> RequestAnswer:
        """Display a menu to add/edit/list players."""

    @abstractmethod
    def show_player_selection(self, players_id: list[str]) -> RequestAnswer:
        """Display a menu to select a player ID."""

    @abstractmethod
    def show_player_registration(self) -> RequestAnswer:
        """Ask first/last name, birthdate and ID."""

    @abstractmethod
    def show_edit_player_menu(self, player_info: dict[str, Any]) -> RequestAnswer:
        """Display a menu to select the attribute to change then an input question."""

    # --- Tournaments methods ---

    @abstractmethod
    def show_manage_tournaments_menu(self) -> RequestAnswer:
        """Display a menu to add/manage/list tournaments."""

    @abstractmethod
    def show_manage_unready_tournament_menu(self, tournament_info: dict[str, Any]) -> RequestAnswer:
        """Display a menu to manage participants or start the selected tournament."""

    @abstractmethod
    def show_manage_tournament_menu(self, tournament_info: dict[str, Any]) -> RequestAnswer:
        """Display a menu to manage rounds and scores of the selected tournament."""

    @abstractmethod
    def keep_or_change_tournament(self, last_edited_tournament: str) -> RequestAnswer:
        """Display a menu to choose between keep editing the last selected tournament or change."""

    @abstractmethod
    def show_tournament_registration(self) -> RequestAnswer:
        """Ask for name, location, dates and rounds number."""

    @abstractmethod
    def how_to_choose_tournament(self, statistics: dict[str, int]) -> RequestAnswer:
        """Display a menu to choose the filter and the method to find an existing tournament."""

    @abstractmethod
    def choose_tournament_by_name(self, tournaments_info: list[tuple[int, str, str]]) -> RequestAnswer:
        """Display an autocomplete question for the tournament name."""

    @abstractmethod
    def choose_tournament_by_list(self, tournaments_info: list[tuple[int, str, str]]) -> RequestAnswer:
        """Display a menu with a list of tournaments to select from."""
