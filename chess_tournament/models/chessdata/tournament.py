from dataclasses import dataclass, field
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
    participants: list[Participant] = field(default_factory=list)
    total_rounds: int = 4
    rounds: list[Round] = field(default_factory=list)
    # necessary ? it is not always the last of the list ?
    # current_round: int | None = None

    @property
    def current_round(self):
        return self.rounds[-1]

    def _generate_pairs(self):
        sorted_participants = sorted(self.participants)
        pairs = []
        n = 0
        while n < len(sorted_participants):
            pairs.append(Match(tuple(sorted_participants[n:n+2])))
            n += 2
        return pairs

    def set_next_round(self):
        print("set next round")
        round = Round(name=f"Round {(len(self.rounds) + 1)}",
                      matches=self._generate_pairs())
        self.rounds.append(round)

    # no neeed end_round, it will be automatically launch after last match
    # end_round will also call set_next_round
    def start_round(self):
        self.current_round.start_round()

    def get_round_matches(self, round_r):
        if not self.rounds or round_r >= len(self.rounds):
            return None
        return self.rounds[round_r].matches

