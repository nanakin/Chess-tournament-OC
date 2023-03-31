from dataclasses import dataclass, field
from datetime import date
from .match import Match
from .participant import Participant
from .round import Round
from ..serialization import Serializable


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

    def _generate_pairs(self):
        sorted_participants = sorted(self.participants)
        pairs = []
        n = 0
        while n < len(sorted_participants):
            pairs.append(Match(tuple(sorted_participants[n:n+2])))
            n += 2
        return pairs

    def set_next_round(self):
        round = Round(name=f"Round {(len(self.rounds) + 1)}",
                      matches=self._generate_pairs())
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
