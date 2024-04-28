from typing import Dict, List, Union

from tourney.team import Team
from tourney.event import Event
from tourney.person import Person
from tourney.competition import Competition, CumulativeScoringMethods


class Tournament:
    def __init__(
        self,
        name: str,
    ):
        pass


class Bracket:
    def __init__(self) -> None:
        self.graph = {}


class BracketCompetition(Competition):
    def __init__(
        self, 
        name: str, 
        events: List[Event], 
        cumulative_scoring_method: CumulativeScoringMethods
    ):
        super().__init__(name, events, cumulative_scoring_method)
        self.round = None
        self.next_competition = None
        self.prev_competition_top = None
        self.prev_competition_bottom = None


class SingleElimination(Tournament):
    def __init__(
        self, 
        name: str,
        seeding: Dict[int, Union[Team, Person]],
    ):
        super().__init__(name)
        self.seeding = seeding
        self.bracket = None

    def generate_bracket(self):
        num_teams = len(self.seeding)
        self.bracket = Bracket()

        # Ensure the number of teams is a power of 2
        if num_teams % 2 == 1:
            # Hold first seed out of the first round
            # Bottom two seeds compete to play first seed
            first_bye = BracketCompetition(

            )
        else:
            # Create initial matchups for the first round
            for i in range(num_teams):
                team_1 = self.seeding[i]
                team_2 = self.seeding[-1*i]
                matchups.append((team_1, team_2))

        # Generate matchups for subsequent rounds
        while len(matchups) > 1:
            new_matchups = []
            for i in range(0, len(matchups), 2):
                winner1, winner2 = matchups[i][0], matchups[i+1][0]
                new_matchups.append((winner1, winner2))
            matchups = new_matchups

        return matchups


class DoubleElimination(Tournament):
    def __init__(self, name: str):
        super().__init__(name)


class BestOf(Tournament):
    def __init__(self, name: str):
        super().__init__(name)


class Swiss(Tournament):
    def __init__(self, name: str):
        super().__init__(name)


class RoundRobin(Tournament):
    def __init__(self, name: str):
        super().__init__(name)


class Gauntlet(Tournament):
    def __init__(self, name: str):
        super().__init__(name)


class Combination(Tournament):
    """Combination of different tournament types"""
    def __init__(self, name: str):
        super().__init__(name)
