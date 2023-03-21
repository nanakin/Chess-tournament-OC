from dataclasses import dataclass, field
from typing import Tuple, List
from datetime import date
from .match import Match
from .participant import Participant
from .round import Round

@dataclass
class Tournament:
    """Tournament data."""
    name: str
    location: str
    begin_date: date
    end_date: date
    participants: Tuple[Participant] | None = None
    total_rounds: int = 4
    rounds: List[Round] = field(default_factory=list)
    # necessary ? it is not always the last of the list ?
    current_round: int | None = None

    def _generate_matches(self) -> Tuple[Match]:
        # sort participants by score and create pairs by order
        # to implement
        return Match((self.participants[0], self.participants[1])),  # temp

    def set_next_round(self):
        round = Round(name=f"Round {self.current_round}",
                      matches=self._generate_matches())
        self.rounds.append(round)
        self.current_round = len(self.rounds) - 1  # not needed ?

    # no neeed end_round, it will be automatically launch after last match
    # end_round will also call set_next_round
    def start_round(self):
        self.rounds[-1].start_round()

    def get_round_matches(self, round_r):
        if not self.rounds or round_r >= len(self.rounds):
            return None
        return self.rounds[round_r].matches