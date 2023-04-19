"""Define common tools that can be used by other Controllers classes."""

from typing import Any

from chess_tournament.models.model import Model
from chess_tournament.views.interface import IView
from chess_tournament.views.requests import Request

from ..helpers import ConjugatedWord, write_list_in_file
from ..states import State


class CommonController:
    """Mixin class defining common tools to be used by other Controller mixin classes."""

    status: State
    model: Model
    view: IView
    context: Any

    def report(self, total: int, data_info: list, conjugated_name: ConjugatedWord, back_state: State) -> None:
        """Show the given list, deal with print and export requests, then back to the previous state."""
        request, _ = self.view.show_list_menu(total, conjugated_name.conjugated_with_number(total))
        if request not in (Request.PRINT, Request.EXPORT):
            self.status = back_state
            return
        if request == Request.PRINT:
            request, _ = self.view.print_list(data_name=conjugated_name.plural, info_list=data_info)
        if request == Request.EXPORT:
            request, request_data = self.view.ask_saving_path()
            if request == Request.SELECTED_PATH:
                filename = request_data
                status_ok, absolute_path = write_list_in_file(data_info, filename, conjugated_name.plural)
                if status_ok:
                    self.view.log(True, f"List correctly saved in {absolute_path}.")
                else:
                    self.view.log(False, f"Cannot save data in {absolute_path}.")
        self.status = back_state
