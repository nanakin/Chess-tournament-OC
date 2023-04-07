from pathlib import Path
from dataclasses import dataclass


@dataclass
class ConjugatedWord:
    singular: str
    plural: str

    def conjugated_with_number(self, number):
        return self.plural if number > 1 else self.singular


def write_list_in_file(data_list, export_path, data_type):
    path = Path(export_path).expanduser()
    if path.is_dir():
        path = path / f"export_{data_type}.txt"
    try:
        with open(path, "w") as f:
            for line in data_list:
                f.write(f"{line}\n")
    except FileNotFoundError:
        return False, path.absolute()
    else:
        return True, path.absolute()
