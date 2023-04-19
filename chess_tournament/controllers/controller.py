"""Define the main Controller behaviour."""

from pathlib import Path

from chess_tournament.models.model import Model
from chess_tournament.views.interface import IView

from .actions import (MainMenuController, MatchesController, ParticipantsController, PlayersController,
                      TournamentsController)
from .states import State


class Controller(
    PlayersController,
    MatchesController,
    TournamentsController,
    ParticipantsController,
    MainMenuController,
):
    """Main Controller class (which inherits from specialized ones)."""

    def __init__(self, view: IView, data_path: Path) -> None:
        """Initialize the controller with the given view and load from backup save."""
        # -- view --
        self.view = view
        # -- model --
        self.model = Model(data_path)
        players_load_log, tournaments_load_log = self.model.load()  # load previous data
        self.view.log(*players_load_log)
        self.view.log(*tournaments_load_log)
        # -- controller --
        self.status = State.MAIN_MENU
        self.context = None  # used to remember the selected tournament

    def run(self) -> None:
        """The main program loop, that execute an action depending on the current program’s state."""
        state_to_action = {
            State.MAIN_MENU: self.show_main_menu,
            State.MANAGE_PLAYER_MENU: self.show_manage_player_menu,
            State.EDIT_PLAYER_MENU: self.show_edit_player_menu,
            State.ADD_PLAYER_MENU: self.show_add_player_menu,
            State.LIST_PLAYERS_MENU: self.show_list_players_menu,
            State.MANAGE_TOURNAMENTS_MENU: self.show_manage_tournaments_menu,
            State.LIST_TOURNAMENTS_MENU: self.show_list_tournaments_menu,
            State.MANAGE_TOURNAMENT_MENU: self.show_manage_tournament_menu,
            State.MANAGE_UNREADY_TOURNAMENT_MENU: self.show_manage_unready_tournament_menu,
            State.ADD_TOURNAMENT_MENU: self.show_tournament_registration,
            State.SELECT_TOURNAMENT_MENU: self.show_select_tournament_menu,
            State.LIST_PARTICIPANTS_MENU: self.show_list_participants_menu,
            State.LIST_MATCHES_MENU: self.show_list_matches_menu,
            State.LIST_ALL_ROUNDS_MENU: self.show_list_all_rounds_menu,
            State.MANAGE_PARTICIPANTS_MENU: self.show_manage_participants_menu,
            State.ADD_PARTICIPANT_MENU: self.show_add_participant_menu,
            State.DELETE_PARTICIPANT_MENU: self.show_delete_participant_menu,
            State.REGISTER_MATCH_SCORE_MENU: self.show_register_match_score_menu,
        }

        while self.status != State.QUIT:
            state_to_action[self.status]()  # execute the action corresponding to the current state
