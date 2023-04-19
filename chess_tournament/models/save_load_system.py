"""Define backup manager class(es) and function(s)."""

from json import JSONDecodeError, dump, load
from pathlib import Path
from typing import Any, Callable

from .chessdata import Player, Tournament

Log = str


def save_at_the_end(players_file: bool = False, tournaments_file: bool = False) -> Callable[[Callable], Callable]:
    """Decorator that saves data to JSON file(s) once the function ended."""

    def save_at_the_end_decorator(function: Callable) -> Callable:
        def wrapper(self, *args, **kwargs) -> Any:
            return_values = function(self, *args, **kwargs)
            self.save(players_file, tournaments_file)
            return return_values

        return wrapper

    return save_at_the_end_decorator


def _make_dirs(directory: Path):
    """Create directories (recursive) for the given paths."""
    if not directory.exists():
        directory.mkdir(exist_ok=True, parents=True)


def save_to_json(data: Any, path: Path) -> tuple[bool, Log]:
    """Write compatible JSON data to JSON file."""
    try:
        with open(path, "w") as json_file:
            dump(data, json_file, indent=2)
    except FileNotFoundError as err:
        return False, f"Unable to save to {path.absolute()} ({err.strerror})"
    else:
        return True, f"autosave in {path.absolute()}"


class BackupManager:
    """Save and load system."""

    players: dict[str, Player]
    tournaments: list[Tournament]

    def __init__(self, path: Path):
        self.data_path = path
        _make_dirs(self.data_path)

    def save(self, players_file: bool = False, tournaments_file: bool = False):
        """Encode model’s data then write them to JSON file(s).

        This function is called by the save_at_the_end decorator used on modifying data Model’s methods."""
        if players_file:
            players_encoded = []
            for player in self.players.values():
                players_encoded.append(player.encode())
            log_status, log_msg = save_to_json(path=(self.data_path / "players.json"), data=players_encoded)
        if tournaments_file:
            tournaments_encoded = []
            for tournament in self.tournaments:
                tournaments_encoded.append(tournament.encode())
            log_status, log_msg = save_to_json(path=(self.data_path / "tournaments.json"), data=tournaments_encoded)

    def load(self) -> tuple[Log, Log]:
        """Load model’s data from JSON files."""
        # TODO: review the function structure

        def json_load_data(filename: Path) -> tuple[tuple[bool, Log], tuple[bool, Log]]:
            """Load data from a given JSON file."""
            with open(filename, "r") as json_file:
                encoded_data = load(json_file)
            return encoded_data

        players_file = self.data_path / "players.json"
        tournaments_file = self.data_path / "tournaments.json"
        try:
            encoded_players = json_load_data(players_file)
        except FileNotFoundError as err:
            status_players_to_log = False, f"No data loaded from {players_file} ({err.strerror})"
        except JSONDecodeError as err:
            status_players_to_log = False, f"Corrupted JSON {players_file} file ({err.msg})"
        else:
            for encoded_player in encoded_players:
                player = Player.decode(encoded_player)
                self.players[player.identifier] = player
            status_players_to_log = True, f"{len(encoded_players)} player(s) loaded from {players_file}"
        try:
            encoded_tournaments = json_load_data(tournaments_file)
        except FileNotFoundError as err:
            status_tournaments_to_log = False, f"No data loaded from {tournaments_file} ({err.strerror})"
        except JSONDecodeError as err:
            status_tournaments_to_log = False, f"Corrupted JSON {tournaments_file} file ({err.msg})"
        else:
            for encoded_tournament in encoded_tournaments:
                tournament = Tournament.decode(encoded_tournament, self.players)
                self.tournaments.append(tournament)
            status_tournaments_to_log = True, f"{len(encoded_tournaments)} tournaments(s) loaded" + \
                                              f" from {tournaments_file}"

        return status_players_to_log, status_tournaments_to_log
