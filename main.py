from chess_tournament.controllers.controller import Controller
import argparse
from pathlib import Path


def main(view_class, data_path):
    view = view_class()
    chess_tournament_manager = Controller(view, data_path)
    chess_tournament_manager.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chess Tournament Manager")
    view_group = parser.add_mutually_exclusive_group()
    view_group.add_argument(
        "-c",
        "--classic",
        action="store_true",
        default=False,
        help="provide a classic input/output user interface",
    )
    view_group.add_argument(
        "-q",
        "--questionary",
        action="store_true",
        default=True,
        help="provide a questionary user interface",
    )
    parser.add_argument("-p", "--data-path", default=(Path(".") / "data"))
    args = parser.parse_args()
    if args.questionary:
        from chess_tournament.views.questionary.view import View
    else:
        from chess_tournament.views.classic.view import View
    main(view_class=View, data_path=args.data_path)
