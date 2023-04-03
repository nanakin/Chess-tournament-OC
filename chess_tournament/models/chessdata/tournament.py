# import itertools
from dataclasses import dataclass, field
from datetime import date
from .match import Match
from .participant import Participant
from .round import Round
from ..serialization import Serializable
import random
from ortools.sat.python import cp_model
from itertools import combinations



# def solve_by_constraints(players_scores, remaining_matches_possibilities):
def solve_by_constraints(participants, remaining_matches_possibilities):
    def weight(participants_pair, match_model_variable):
        return match_model_variable * (abs(participants_pair[0].score - participants_pair[1].score) ** 2)

    # in formal methods, a SAT solver aims to solve the boolean satisfiability (SAT) problem
    # cp = Constraint Programming
    # here we want :
    # - to select exactly one match per player from all possible (remaining) combination of 2
    # - to consider the global minimal score difference between players (calculated for each possibility)
    model = cp_model.CpModel()
    solver = cp_model.CpSolver()

    matches_model_variables = {}
    for match in remaining_matches_possibilities:
        # specify to model that a match (e.g. pairing players A & B) can be True or False (i.e. selected or not)
        match_model_variable = model.NewBoolVar(f"{str(match[0])}-{str(match[1])}")
        matches_model_variables[match] = match_model_variable
    print(f"{matches_model_variables=}")

    # specify to model the constraint that only one match per player can be selected at the same time
    # e.g. AB or AC or AD (i.e. AB + AC + AD = 1)
    for player in participants:
        player_matches_model_variables = [
            model_variable for match, model_variable in matches_model_variables.items()
            if player in match]
        model.Add(sum(player_matches_model_variables) == 1)

    # specify to model how to select the best choice by giving a weight to each possibility
    # here based on players scores difference
    model.Minimize(
        sum((weight(players_pair, match_model_variable)
             for players_pair, match_model_variable in matches_model_variables.items())))

    # call the solver to find the best solution respecting the given constraints
    # i.e. selecting exactly one match per player AND selecting minimal weight)
    status = solver.Solve(model)
    if status == cp_model.OPTIMAL:
        solution = [players_pair for players_pair, match_var in matches_model_variables.items()
                    if solver.Value(match_var)]
    else:
        solution = None
    return solution


@dataclass
class Tournament(Serializable):
    """Tournament data."""
    name: str
    location: str
    begin_date: date
    end_date: date
    participants: list[Participant] = field(default_factory=list)
    total_rounds: int = 4
    rounds: list[Round] = field(default_factory=list)
    _remaining_matches_possibilities = None
    # necessary ? it is not always the last of the list ?
    # current_round: int | None = None

    @property
    def total_finished_rounds(self):
        if not self.rounds:
            return 0
        else:
            return len(self.rounds) - 1 if self.rounds[-1].end_time is None else len(self.rounds)

    def __str__(self):
        return (f'Tournament "{self.name}" located in {self.location} from {str(self.begin_date)} to {str(self.end_date)}'
                f'. {len(self.participants)} participants. {self.total_rounds} rounds ({self.total_finished_rounds}/{self.total_rounds} finished).')

    def __lt__(self, other):
        return self.begin_date < other.begin_date

    @property
    def current_round(self):
        return self.rounds[-1] if self.rounds else None

    @property
    def is_ended(self):
        return self.total_finished_rounds == self.total_rounds

    @property
    def total_started_rounds(self):
        return len(self.rounds)

    def _generate_pairs_random(self):
        shuffled_participants = random.sample(self.participants, len(self.participants))
        # to-do replace by list(zip(u[::2], u[1::2]))
        # or use
        # def n_clusters(iterable, n=2):
        #     return zip(*[iter(iterable)] * n)
        pairs = []
        n = 0
        while n < len(shuffled_participants):
            pairs.append(tuple(shuffled_participants[n:n + 2]))
            n += 2
        return pairs

    def _generate_pairs_from_score(self):
        pairs = solve_by_constraints(self.participants, self._remaining_matches_possibilities)
        return pairs

    def _generate_pairs(self):
        if self._remaining_matches_possibilities is None or not self._remaining_matches_possibilities:
            self._generate_all_matches_possibilities()

        if self.total_started_rounds == 0:
            pairs_list = self._generate_pairs_random()
        else:
            pairs_list = self._generate_pairs_from_score()

        self._update_remaining_matches_possibilities(pairs_list)
        return tuple(Match(pair) for pair in pairs_list)

    def _update_remaining_matches_possibilities(self, matches_list):
        self._remaining_matches_possibilities -= set(matches_list)

    def _generate_all_matches_possibilities(self):
        self._remaining_matches_possibilities = set(combinations(self.participants, 2))

    def set_next_round(self):
        matches_list = self._generate_pairs()
        round = Round(name=f"Round {(len(self.rounds) + 1)}",
                      matches=matches_list)
        self.rounds.append(round)

    # no neeed end_round, it will be automatically launch after last match
    # end_round will also call set_next_round
    def start_round(self):
        if not self.current_round:
            self.set_next_round()
        self.current_round.start_round()

    def get_round_matches(self, round_r):
        if not self.rounds or round_r >= len(self.rounds):
            return None
        return self.rounds[round_r].matches

    def encode(self):
        return {
            "name": self.name,
            "location": self.location,
            "begin_date": str(self.begin_date),
            "end_date": str(self.end_date),
            "total_rounds": self.total_rounds,
            "participants": [participant.encode() for participant in self.participants],
            "rounds": [round.encode() for round in self.rounds]
        }

    @classmethod
    def decode(cls, encoded_data):
        encoded_data["begin_date"] = date.fromisoformat(encoded_data["begin_date"])
        encoded_data["end_date"] = date.fromisoformat(encoded_data["end_date"])
        encoded_data["rounds"] = [Round.decode(encoded_round)
                                  for encoded_round in encoded_data["rounds"]]
        encoded_data["participants"] = [Participant.decode(encoded_participant)
                                        for encoded_participant in encoded_data["participants"]]
        return cls(**encoded_data)
