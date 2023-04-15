"""Define the chess manager entry point and main function."""
from chess_tournament.controllers.controller import Controller
from chess_tournament.views.questionary.view import View
import argparse
from pathlib import Path


def main(view_class, data_path):
    """Main program function that initializes the view and the controller then call its main function loop."""
    view = view_class()
    chess_tournament_manager = Controller(view, data_path)
    chess_tournament_manager.run()


if __name__ == "__main__":
    # Program entry point that parses optional argument then call the main function.
    parser = argparse.ArgumentParser(description="Chess Tournament Manager")
    parser.add_argument("-p", "--data-path", default=(Path(".") / "data"))
    args = parser.parse_args()
    main(view_class=View, data_path=args.data_path)
