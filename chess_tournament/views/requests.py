from enum import Enum
from typing import TypeAlias

Request = Enum("Request", [
    "EXIT_APP",
    "EXIT_LOCAL_MENU",
    "LAUNCH_PLAYER_MENU",
    "ADD_PLAYER",
    "LAUNCH_TOURNAMENT_MENU",
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
