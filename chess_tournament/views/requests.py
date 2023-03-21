from enum import Enum
from typing import TypeAlias

Request = Enum("Request", [
    "EXIT_APP",
    "EXIT_LOCAL_MENU",
    "LAUNCH_PLAYER_MENU",
    "ADD_PLAYER",
    "LAUNCH_TOURNAMENT_MENU",
    "ADD_TOURNAMENT"
])

RequestAnswer: TypeAlias = Request | tuple[Request, list[object]]
