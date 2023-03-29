import questionary as q
from ..requests import Request, RequestAnswer

class MatchesMenus:

    def show_matches(self, matches):
        print("List of matches :")
        for match in matches:
            print(match)


    def select_match(self, matches_info) -> RequestAnswer:
        print(matches_info)
        question = q.select(
            "Which match ?",
            choices=matches_info)
        #   q.Separator(),
        #   q.Choice(title="Back", value=Request.MANAGE_TOURNAMENT)])
        answer = question.ask()
        if answer:
            return Request.SELECTED_MATCH, matches_info.index(answer)
        else:
            return Request.MANAGE_TOURNAMENT, None


    def enter_score(self, match_info) -> RequestAnswer:
        # to-do : print the first player info or detail the 2 names in the choices
        question = q.select(
            "Select the result of the match, for the first player",
            choices=["WIN", "LOSE", "DRAW"])
        answer = question.ask()
        if answer:
            return Request.ADD_MATCH_RESULT, answer
        else:
            return Request.MANAGE_TOURNAMENT, None