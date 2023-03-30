from pathlib import Path


def write_list_in_file(data_list, export_path, data_type):
    path = Path(export_path)
    if path.is_dir():
        path = path / f"export_{data_type}.txt"
    try:
        with open(path, 'w') as f:
            for line in data_list:
                f.write(f"{line}\n")
    except FileNotFoundError:
        return False, None
    else:
        return True, path.absolute()
