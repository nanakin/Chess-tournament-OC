from enum import Enum
from typing import TypeAlias

Request = Enum("Request", [
    "EXIT_APP",
    "EXIT_LOCAL_MENU",
    "MAIN_MENU",
    "SAVE",
    "MANAGE_PLAYER",
    "ADD_PLAYER",
    "REGISTER_PLAYER_DATA",
    "LIST_PLAYERS",
    "EDIT_PLAYER",
    "PRINT_PLAYERS",
    "EXPORT_PLAYERS",
    "SHOW_SELECT_PLAYER",
    "SELECTED_PLAYER",
    "CONFIRM",
    "SHOW_CONFIRM_PLAYER",
    "SHOW_EDIT_PLAYER_MENU",
    "MANAGE_TOURNAMENT",
    "ADD_TOURNAMENT",
    "LAUNCH_PARTICIPANT_MENU",
    "ADD_PARTICIPANT",
    "GET_MATCHES_LIST",
    "REGISTER_MATCH_SCORE",
    "CHOSEN_TOURNAMENT",
    "CHOSEN_MATCH",
    "CHOSEN_ROUND",
    "ADD_MATCH_RESULT"
])

RequestAnswer: TypeAlias = Request | tuple[Request, list[object]]
