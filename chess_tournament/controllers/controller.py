"""Define the main Controller behaviour."""

from chess_tournament.models.model import Model
from .states import State
from .actions.players import PlayersController
from .actions.matches import MatchesController
from .actions.tournaments import TournamentsController
from .actions.participants import ParticipantsController
from .actions.main import MainMenuController


class Controller(
    PlayersController,
    MatchesController,
    TournamentsController,
    ParticipantsController,
    MainMenuController,
):
    """Main Controller class (which inherits from specialized ones)."""

    def __init__(self, view, data_path):
        """Initialize the controller with the given view and load from backup save."""
        # view
        self.view = view

        # model
        self.model = Model(data_path)
        total_players_loaded, total_tournaments_loaded = self.model.load()
        self.view.log(
            bool(total_players_loaded),
            f"{total_players_loaded} players loaded from save file.",
        )
        self.view.log(
            bool(total_tournaments_loaded),
            f"{total_tournaments_loaded} tournaments loaded from save file.",
        )

        # controller
        self.status = State.MAIN_MENU
        self.context = None

    def run(self):
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
