"""Define helping function(s) and class(es) used by the controllers classes."""

from dataclasses import dataclass
from pathlib import Path

CompleteLog = tuple[bool, str]

@dataclass
class ConjugatedWord:
    """Simplify the conjugation management in console and log printed messages."""

    singular: str
    plural: str

    def conjugated_with_number(self, number: int) -> str:
        return self.plural if number > 1 else self.singular


def write_list_in_file(data_list: list, export_path: Path, data_type: str) -> CompleteLog:
    """Save the given data list in the given path."""
    path = export_path.expanduser()
    if path.is_dir():
        path = path / f"export_{data_type}.txt"
    try:
        with open(path, "w") as f:
            for line in data_list:
                f.write(f"{line}\n")
    except FileNotFoundError:
        return False, str(path.absolute())
    else:
        return True, str(path.absolute())
