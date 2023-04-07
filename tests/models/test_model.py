import datetime

from chess_tournament.models.model import Player, Participant, Match, Round, Tournament
import pytest
from datetime import datetime

# Player ----------------------------------------------------------------------


@pytest.fixture
def player_a():
    player_parameters = {
        "first_name": "Marie",
        "last_name": "Dupont",
        "birth_date": datetime(1980, 1, 2),
    }
    return Player(**player_parameters)


@pytest.fixture
def player_b():
    player_parameters = {
        "first_name": "Boris",
        "last_name": "Jackson",
        "birth_date": datetime(1970, 12, 30),
    }
    return Player(**player_parameters)


# Participant -----------------------------------------------------------------


@pytest.fixture
def participant_a(player_a):
    participant_parameters = {"player": player_a}
    return Participant(**participant_parameters)


@pytest.fixture
def participant_b(player_b):
    participant_parameters = {"player": player_b}
    return Participant(**participant_parameters)


def test_add_score_to_participant(participant_a):
    participant_a.add_score(10)
    assert participant_a.score == 10  # to do : use a getter


# Match -----------------------------------------------------------------------


@pytest.fixture
def match_a(participant_a, participant_b):
    return Match((participant_a, participant_b))


def test_match_register_score(match_a):
    scores = (Match.Points.WIN, Match.Points.LOSE)
    match_a.register_score(scores)
    assert (
        match_a.participants_scores[0].value,
        match_a.participants_scores[1].value,
    ) == (
        Match.Points.WIN.value,
        Match.Points.LOSE.value,
    )  # to do : use a getter


# Round -----------------------------------------------------------------------


@pytest.fixture
def round_a(match_a):
    round_parameters = {"name": "Round A", "matches": (match_a,)}
    return Round(**round_parameters)


# add tests for start and end methods using a mock ?

# Tournament ------------------------------------------------------------------


@pytest.fixture
def tournament_a(player_a, player_b):
    tournament_parameters = {
        "name": "Word Cup 2023",
        "location": "France, Bordeaux",
        "begin_date": datetime(2023, 11, 5),
        "end_date": datetime(2023, 11, 25),
        "participants": (player_a, player_b),
    }
    return Tournament(**tournament_parameters)


def test_get_next_round(tournament_a):
    tournament_a.get_next_round()
    matches = tournament_a.rounds[tournament_a.current_round]
    assert len(matches.matches) == len(tournament_a.participants) // 2
