"""Define common tools that can be used by other Controllers classes."""

from chess_tournament.models.model import Model
from chess_tournament.views.requests import Request
from chess_tournament.views.interface import IView
from ..states import State
from ..helpers import ConjugatedWord, write_list_in_file
from typing import Any


class CommonController:
    """Mixin class defining common tools to be used by other Controller mixin classes."""

    status: State
    model: Model
    view: IView
    context: Any

    def report(self, total, data_info, conjugated_name: ConjugatedWord, back_state):
        """Show the given list, deal with print and export requests, then back to the previous state."""
        action = self.view.show_list_menu(total, conjugated_name.conjugated_with_number(total))
        if action not in (Request.PRINT, Request.EXPORT):
            self.status = back_state
            return
        if action == Request.PRINT:
            action = self.view.print_list(data_name=conjugated_name.plural, info_list=data_info)
        if action == Request.EXPORT:
            action, action_data = self.view.ask_saving_path()
            if action == Request.SELECTED_PATH:
                filename = action_data
                status_ok, absolute_path = write_list_in_file(data_info, filename, conjugated_name.plural)
                if status_ok:
                    self.view.log(True, f"List correctly saved in {absolute_path}.")
                else:
                    self.view.log(False, f"Cannot save data in {absolute_path}.")
        self.status = back_state
