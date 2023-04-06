from enum import Enum, auto

class State(Enum):
        MAIN_MENU = auto(),
        MANAGE_PLAYER_MENU = auto(),
        ADD_PLAYER_MENU = auto(),
        EDIT_PLAYER_MENU = auto(),
        LIST_PLAYERS_MENU = auto(),
        MANAGE_TOURNAMENTS_MENU = auto(),
        LIST_TOURNAMENTS_MENU = auto(),
        ADD_TOURNAMENT_MENU = auto(),
        REGISTER_MATCH_SCORE_MENU = auto(),
        LIST_PARTICIPANTS_MENU = auto(),
        LIST_MATCHES_MENU = auto(),
        LIST_ALL_ROUNDS_MENU = auto(),
        ADD_PARTICIPANT_MENU = auto(),
        DELETE_PARTICIPANT_MENU = auto(),
        MANAGE_PARTICIPANTS_MENU = auto(),
        MANAGE_TOURNAMENT_MENU = auto(),
        MANAGE_UNREADY_TOURNAMENT_MENU = auto(),
        SELECT_TOURNAMENT_MENU = auto(),
        QUIT = auto()
