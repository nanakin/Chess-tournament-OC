"""Define tournaments related data structures."""

from dataclasses import dataclass, field
from datetime import date
from .match import Match
from .participant import Participant
from .round import Round
from ..serialization import Serializable
import random
from ortools.sat.python import cp_model
from itertools import combinations
import logging


def solve_by_constraints(participants, remaining_matches_possibilities):
    """Return a list of participants pairs generated using a constraints solver.

    in formal methods, a SAT solver aims to solve the boolean satisfiability (SAT) problem
    cp = Constraint Programming
    here we want :
    - to select exactly one match per player from all possible (remaining) combination of 2
    - to consider the global minimal score difference between players (calculated for each possibility)
    """
    def weight(participants_pair, match_model_variable):
        """Privilege the smallest score gaps for matchmaking."""
        return match_model_variable * (abs(participants_pair[0].score - participants_pair[1].score) ** 2)

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

    @property
    def total_finished_rounds(self):
        """Return the total number of finished rounds."""
        if not self.rounds:
            return 0
        else:
            return len(self.rounds) - 1 if self.rounds[-1].end_time is None else len(self.rounds)

    def __str__(self):
        """Return the string representation of the tournament instance."""
        return f'{self.name} in {self.location} ({str(self.begin_date)} > {str(self.end_date)})'

    def __lt__(self, other):
        """Order tournaments by starting date."""
        return self.begin_date < other.begin_date

    @property
    def current_round(self):
        """Return the last started round."""
        return self.rounds[-1] if self.rounds else None

    @property
    def is_ended(self):
        """Return True if all rounds are finished, False otherwise."""
        return self.total_finished_rounds == self.total_rounds

    @property
    def is_started(self):
        """Return True if a least one round has been generated, False otherwise."""
        return self.total_started_rounds > 0

    @property
    def total_started_rounds(self):
        """Return the total number of rounds generated."""
        return len(self.rounds)

    def _generate_pairs_random(self):
        """Generate list of participant pairs with a random matchmaking."""
        shuffled_participants = random.sample(self.participants, len(self.participants))
        pairs = list(zip(shuffled_participants[::2], shuffled_participants[1::2]))
        return pairs

    def _generate_pairs_from_score(self):
        """Generate list of participant pairs using a constraints solver to do the matchmaking."""
        pairs = solve_by_constraints(self.participants, self._remaining_matches_possibilities)
        return pairs

    def _generate_pairs(self):
        """Do the matchmaking by generating list of participant pairs (matches)."""

        # generate all possibilities of matches pairs
        # (it is useful for the matchmaking by score and to avoid duplicate encounters)
        # initialized at the first round and when the list of remaining possibilities is exhausted
        if self._remaining_matches_possibilities is None or not self._remaining_matches_possibilities:
            self._generate_all_matches_possibilities()

        if self.total_started_rounds == 0:
            pairs_list = self._generate_pairs_random()  # first round is generated randomly
        else:
            pairs_list = (
                self._generate_pairs_from_score()
            )  # after the first round, matchmaking is realized by a solver

        self._update_remaining_matches_possibilities(pairs_list)  # to avoid duplicate encounters
        return tuple(Match(pair) for pair in pairs_list)

    def _update_remaining_matches_possibilities(self, matches_list):
        """Remove current round matches from the not done/remaining matches possibilities."""
        self._remaining_matches_possibilities -= set(matches_list)

    def _generate_all_matches_possibilities(self):
        """Generate all possible combination of 2 from a list of participants."""
        self._remaining_matches_possibilities = set(combinations(self.participants, 2))

    def set_next_round(self):
        """Do the matchmaking and register the round internally."""
        matches_list = self._generate_pairs()
        logging.debug(f"Generated matches list for round {self.total_started_rounds + 1}:")
        for match in matches_list:
            logging.debug(f"{str(match.participants_pair[0])} vs {str(match.participants_pair[1])}")
        round = Round(name=f"Round {(len(self.rounds) + 1)}", matches=matches_list)
        self.rounds.append(round)

    def start_round(self):
        """Register the starting time of the current round."""
        if not self.current_round:  # TODO: verify if it can happen
            self.set_next_round()
        self.current_round.start_round()

    def get_round_matches(self, round_r):
        """Return matches of the given round index."""
        if not self.rounds or round_r >= len(self.rounds):
            return None
        return self.rounds[round_r].matches

    def encode(self):
        """Transform the instance of the object into JSON compatible format."""
        return {
            "name": self.name,
            "location": self.location,
            "begin_date": str(self.begin_date),
            "end_date": str(self.end_date),
            "total_rounds": int(self.total_rounds),
            "participants": [participant.encode() for participant in self.participants],
            "rounds": [round.encode() for round in self.rounds],
        }

    @classmethod
    def decode(cls, encoded_data, players_db):
        """Instantiate a new object from data in JSON format."""
        encoded_data["begin_date"] = date.fromisoformat(encoded_data["begin_date"])
        encoded_data["end_date"] = date.fromisoformat(encoded_data["end_date"])
        encoded_data["participants"] = [
            Participant.decode(encoded_participant, players_db) for encoded_participant in encoded_data["participants"]
        ]
        encoded_data["rounds"] = [Round.decode(encoded_round, encoded_data["participants"]) for encoded_round in encoded_data["rounds"]]
        return cls(**encoded_data)
