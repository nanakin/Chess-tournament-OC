from enum import Enum, auto
from typing import Any


class Request(Enum):
    """List of allowed view requests."""

    EXIT_APP = auto()
    EXIT_LOCAL_MENU = auto()
    MAIN_MENU = auto()
    SAVE = auto()
    MANAGE_PLAYER = auto()
    ADD_PLAYER = auto()
    REGISTER_PLAYER_DATA = auto()
    LIST_PLAYERS = auto()
    EDIT_PLAYER = auto()
    SELECTED_PLAYER = auto()
    CONFIRM = auto()
    MANAGE_TOURNAMENT = auto()
    GENERATE_MATCHES = auto()
    ADD_TOURNAMENT = auto()
    EDIT_TOURNAMENT = auto()
    LIST_TOURNAMENTS = auto()
    START_ROUND = auto()
    PRINT = auto()
    EXPORT = auto()
    KEEP_SELECTED_TOURNAMENT = auto()
    CHANGE_SELECTED_TOURNAMENT = auto()
    REGISTER_TOURNAMENT_DATA = auto()
    SELECTED_PATH = auto()
    LIST_MATCHES = auto()
    MANAGE_PARTICIPANTS = auto()
    ADD_PARTICIPANT = auto()
    DELETE_PARTICIPANT = auto()
    LIST_PARTICIPANTS = auto()
    REGISTER_MATCH_SCORE = auto()
    SELECTED_MATCH = auto()
    SELECTED_TOURNAMENT = auto()
    LIST_ROUNDS_SCORES = auto()
    ADD_MATCH_RESULT = auto()
    FIND_TOURNAMENT_BY_NAME = auto()
    FIND_TOURNAMENT_BY_LIST_ONGOING = auto()
    FIND_TOURNAMENT_BY_LIST_FUTURE = auto()
    FIND_TOURNAMENT_BY_LIST_PAST = auto()
    FIND_TOURNAMENT_BY_LIST_ALL = auto()


RequestAnswer = tuple[Request, Any]


def valid_request_or_exit(check: Any, return_if_ok: Request | RequestAnswer) -> RequestAnswer:
    """Return a valid request for the controller (particularly useful with Ctrl-C)."""
    return_if_not_ok = (Request.EXIT_LOCAL_MENU, None)
    if not isinstance(return_if_ok, tuple):
        return_if_ok = (return_if_ok, None)
    return return_if_ok if check else return_if_not_ok
