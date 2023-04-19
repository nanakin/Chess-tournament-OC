import random
from itertools import combinations

from ortools.sat.python import cp_model

from ..chessdata import Match, Participant, Round


def solve_by_constraints(
    participants: list[Participant], remaining_matches_possibilities: set[tuple[Participant, Participant]]
) -> list[tuple[Participant, Participant]] | None:
    """Return a list of participants pairs generated using constraints solver.

    in formal methods, a SAT solver aims to solve the boolean satisfiability (SAT) problem
    cp = Constraint Programming
    here we want :
    - to select exactly one match per player from all possible (remaining) combination of 2
    - to consider the global minimal score difference between players (calculated for each possibility)
    """

    def weight(participants_pair: tuple[Participant, Participant], match_model_variable: cp_model.IntVar) -> int:
        """Privilege the smallest score gaps for matchmaking."""
        return match_model_variable * (abs(participants_pair[0].score - participants_pair[1].score) ** 2)

    model = cp_model.CpModel()
    solver = cp_model.CpSolver()

    matches_model_variables = {}
    for match in remaining_matches_possibilities:
        # specify to model that a match (e.g. pairing players A & B) can be True or False (i.e. selected or not)
        match_model_variable = model.NewBoolVar(f"{str(match[0])}-{str(match[1])}")
        matches_model_variables[match] = match_model_variable

    # specify to model the constraint that only one match per player can be selected at the same time
    # e.g. AB or AC or AD (i.e. AB + AC + AD = 1)
    for player in participants:
        player_matches_model_variables = [
            model_variable for match, model_variable in matches_model_variables.items() if player in match
        ]
        model.Add(sum(player_matches_model_variables) == 1)

    # specify to model how to select the best choice by giving a weight to each possibility
    # here based on players scores difference
    model.Minimize(
        sum(
            (
                weight(players_pair, match_model_variable)
                for players_pair, match_model_variable in matches_model_variables.items()
            )
        )
    )

    # call the solver to find the best solution respecting the given constraints
    # i.e. selecting exactly one match per player AND selecting minimal weight
    status = solver.Solve(model)
    if status == cp_model.OPTIMAL:
        solution = [
            players_pair for players_pair, match_var in matches_model_variables.items() if solver.Value(match_var)
        ]
    else:
        solution = None
    return solution


class MatchMaking:
    """Do the matchmaking by generating list of participant pairs (matches)."""

    def __init__(self) -> None:
        self._remaining_matches_possibilities: set[tuple[Participant, Participant]] = set()

    def _update_remaining_matches_possibilities(self, matches_list: list[tuple[Participant, Participant]]) -> None:
        """Remove current round matches from the not done/remaining matches possibilities."""
        self._remaining_matches_possibilities -= set(matches_list)

    def reconstruct_remaining_possibilities_from_past_matches(
        self, participants: list[Participant], rounds: list[Round]
    ) -> None:
        self._generate_all_matches_possibilities(participants)
        past_pairs = [match.participants_pair for round in rounds for match in round.matches]
        self._update_remaining_matches_possibilities(past_pairs)

    def _generate_all_matches_possibilities(self, participants: list[Participant]) -> None:
        """Generate all possible combination of 2 from a list of participants."""
        self._remaining_matches_possibilities = set(combinations(participants, 2))

    @staticmethod
    def _generate_pairs_random(participants: list[Participant]) -> list[tuple[Participant, Participant]]:
        """Generate list of participant pairs with a random matchmaking."""
        shuffled_participants = random.sample(participants, len(participants))
        pairs = list(zip(shuffled_participants[::2], shuffled_participants[1::2]))
        return pairs

    def _generate_pairs_from_score(self, participants: list[Participant]) -> list[tuple[Participant, Participant]]:
        """Generate list of participant pairs using a constraints solver to do the matchmaking."""

        # generate all possibilities of matches pairs
        # (it is useful for the matchmaking by score and to avoid duplicate encounters)
        # initialized at the first round and when the list of remaining possibilities is exhausted
        if self._remaining_matches_possibilities is None or not self._remaining_matches_possibilities:
            self._generate_all_matches_possibilities(participants)

        pairs = solve_by_constraints(participants, self._remaining_matches_possibilities)

        if pairs is None:  # no solution with the given constraints
            self._generate_all_matches_possibilities(participants)  # safety-net
            pairs = self._generate_pairs_from_score(participants)
        return pairs

    def generate_pairs(self, total_started_rounds: int, participants: list[Participant]) -> tuple[Match, ...]:
        """Do the matchmaking by generating list of participant pairs (matches)."""

        if total_started_rounds == 0:
            pairs_list = self._generate_pairs_random(participants)  # first round is generated randomly
        else:
            # after the first round, matchmaking is realized by a solver
            pairs_list = self._generate_pairs_from_score(participants)

        self._update_remaining_matches_possibilities(pairs_list)  # to avoid duplicate encounters
        return tuple(Match(pair) for pair in pairs_list)
