"""Define the interface for all the views classes, these methods will be used by the controller."""
from abc import ABC

from .requests import RequestAnswer


class IView(ABC):
    """A "valid" view must implements the following methods."""

    # --- common methods ---

    def log(self, ok_status, to_print=None):
        """Add a log to the log queue."""

    def show_log(self):
        """Display logs and purge the queue."""

    def show_confirmation(self, to_confirm) -> RequestAnswer:
        """Display a yes/no question."""

    def ask_saving_path(self) -> RequestAnswer:
        """Display an autocomplete path input."""

    def show_list_menu(self, total, data_name) -> RequestAnswer:
        """Display a menu to print or export a list."""

    def print_list(self, data_name, info_list) -> RequestAnswer:
        """Display the given list then suggest to export it."""

    # --- main menu method ---

    def show_main_menu(self) -> RequestAnswer:
        """Display the main menu."""

    # --- matches methods ---

    def select_match(self, matches_info) -> RequestAnswer:
        """Display a menu with the round’s matches list."""

    def enter_score(self, players) -> RequestAnswer:
        """Display a menu to select the participants score (WIN/LOSE/DRAW)."""

    # --- participants methods ---

    def show_manage_participants_menu(self, total_participants) -> RequestAnswer:
        """Display a menu to manage participants."""

    # --- players methods ---

    def show_manage_player_menu(self) -> RequestAnswer:
        """Display a menu to add/edit/list players."""

    def show_player_selection(self, players_id) -> RequestAnswer:
        """Display a menu to select a player ID."""

    def show_player_registration(self) -> RequestAnswer:
        """Ask first/last name, birthdate and ID."""

    def show_edit_player_menu(self, player_info) -> RequestAnswer:
        """Display a menu to select the attribute to change then an input question."""

    # --- Tournaments methods ---

    def show_manage_tournaments_menu(self) -> RequestAnswer:
        """Display a menu to add/manage/list tournaments."""

    def show_manage_unready_tournament_menu(self, tournament_info) -> RequestAnswer:
        """Display a menu to manage participants or start the selected tournament."""

    def show_manage_tournament_menu(self, tournament_info) -> RequestAnswer:
        """Display a menu to manage rounds and scores of the selected tournament."""

    def keep_or_change_tournament(self, last_edited_tournament) -> RequestAnswer:
        """Display a menu to choose between keep editing the last selected tournament or change."""

    def show_tournament_registration(self) -> RequestAnswer:
        """Ask for name, location, dates and rounds number."""

    def how_to_choose_tournament(self, statistics) -> RequestAnswer:
        """Display a menu to choose the filter and the method to find an existing tournament."""

    def choose_tournament_by_name(self, tournaments_info) -> RequestAnswer:
        """Display an autocomplete question for the tournament name."""

    def choose_tournament_by_list(self, tournaments_info) -> RequestAnswer:
        """Display a menu with a list of tournaments to select from."""
