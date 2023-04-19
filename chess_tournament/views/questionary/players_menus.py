"""Define chess players related user interface."""

import questionary as q
from typing import Any

from ..requests import Request, RequestAnswer, valid_request_or_exit
from ..validators import national_identifier_validator, non_empty_alphabet_validator, past_date_validator
from .common import clear_screen_and_show_log, print_title


class PlayerMenus:
    """Players related View’s mixin class."""

    @clear_screen_and_show_log
    def show_manage_player_menu(self) -> RequestAnswer:
        """Display a select menu : add/edit/list players or back."""
        print_title("Players menu")
        question = q.select(
            "What do you want to do ?",
            choices=[
                q.Choice(title="Add player", value=Request.ADD_PLAYER),
                q.Choice(title="Edit player", value=Request.EDIT_PLAYER),
                q.Choice(title="List players", value=Request.LIST_PLAYERS),
                q.Separator(),
                q.Choice(title="Back", value=Request.MAIN_MENU),
            ],
        )
        answer = question.ask()
        return valid_request_or_exit(check=answer, return_if_ok=answer)

    @clear_screen_and_show_log
    def show_player_selection(self, players_id: list[str]) -> RequestAnswer:
        """Display an autocomplete question for players ID."""
        print_title("Player selection menu")
        question = q.autocomplete(
            "Enter the player ID :",
            choices=players_id,
            validate=lambda x: x in players_id,
        )
        answer = question.ask()
        return valid_request_or_exit(check=answer, return_if_ok=(Request.SELECTED_PLAYER, answer))

    @clear_screen_and_show_log
    def show_player_registration(self) -> RequestAnswer:
        """Prompt 4 input questions (first/last name, birthdate, ID) with user entries validation."""
        print_title("Player registration menu")
        add_player_questions = [
            {
                "type": "text",
                "name": "first_name",
                "qmark": ">",
                "message": "Enter player's first name :",
                "validate": non_empty_alphabet_validator,
            },
            {
                "type": "text",
                "name": "last_name",
                "qmark": ">",
                "message": "Enter player's last name :",
                "validate": non_empty_alphabet_validator,
            },
            {
                "type": "text",
                "name": "birth_date",
                "qmark": ">",
                "message": "Enter player's date of birth (YYYY-MM-DD):",
                "validate": past_date_validator,
            },
            {
                "type": "text",
                "name": "identifier",
                "qmark": ">",
                "message": "Enter player's national identifier (AB12345):",
                "validate": national_identifier_validator,
            },
        ]
        raw_player_data = q.prompt(add_player_questions)
        return valid_request_or_exit(check=raw_player_data,
                                     return_if_ok=(Request.REGISTER_PLAYER_DATA, raw_player_data))

    @clear_screen_and_show_log
    def show_edit_player_menu(self, player_info: dict[str, Any]) -> RequestAnswer:
        """Display a menu to select the attribute to change then an input question (with user entry validation)."""
        print_title("Player edition menu")
        what_to_edit = q.select(
            "What to edit ?",
            choices=[
                q.Choice(title="First name", value="first_name"),
                q.Choice(title="Last name", value="last_name"),
                q.Choice(title="Birth date", value="birth_date"),
                q.Choice(title="Cancel"),
            ],
        )
        answer = what_to_edit.ask()
        if answer == "first_name":
            player_info["first_name"] = q.text(
                "Enter player's new first name: ", validate=non_empty_alphabet_validator
            ).ask()
        elif answer == "last_name":
            player_info["last_name"] = q.text(
                "Enter player's new last name: ", validate=non_empty_alphabet_validator
            ).ask()
        elif answer == "birth_date":
            player_info["birth_date"] = q.text("Enter player's new birth date: ", validate=past_date_validator).ask()

        return valid_request_or_exit(check=bool(answer in player_info),
                                     return_if_ok=(Request.REGISTER_PLAYER_DATA, player_info))
