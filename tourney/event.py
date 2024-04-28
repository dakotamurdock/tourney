from datetime import datetime
from typing import Callable, Dict, List, Optional, Union
from uuid import uuid1

import pandas as pd

from tourney.person import Person
from tourney.team import Team, Group


class Event:
    def __init__(
        self,
        name: str,
        participants: List[Union[Team, Person]],
        group_scoring_functions: Union[Callable, Dict[Group, Callable]] = None,
        team_scoring_function: Callable = None,
        person_level_scoring: bool = False,
        scoring_unit: Optional[str] = None,
        datetime_start: Optional[datetime] = None,
        datetime_end: Optional[datetime] = None,
        duration: Optional[int] = None,
        duration_unit: Optional[str] = None,
    ):
        self.id = str(uuid1())
        self.name = name

        self.datetime_start = datetime_start
        self.datetime_end = datetime_end
        self.duration = duration
        self.duration_unit = duration_unit

        self.participants = participants

        self.person_level_scoring = person_level_scoring
        self.group_scoring_functions = group_scoring_functions
        self.team_scoring_function = team_scoring_function
        self.scoring_unit = scoring_unit

        # Determine if working with teams (and groups) or individuals in event scoring
        self.team_scoring = False
        self.group_scoring = False
        if isinstance(self.participants[0], Team):
            self.team_scoring = True
            if self.participants[0].groups:
                self.group_scoring = True
        else:
            self.person_level_scoring = True

        # Initialize Scoring Dictionary
        if self.team_scoring:
            if self.group_scoring:
                if self.person_level_scoring:
                    # Individuals on a team are divided into sub-groups
                    # Scoring tracked at the person level
                    scoring_records = []
                    for team in self.participants:
                        for group in team.groups:
                            for person in group.roster:
                                scoring_records.append(
                                    {"team": team.uuid, "group": group.uuid, "person": person.uuid, "score": None}
                                )
                    self.scoring_table = pd.DataFrame.from_dict(scoring_records)
                else:
                    # Individuals on a team are divided into groups
                    # Scored at the group level
                    scoring_records = []
                    for team in self.participants:
                        for group in team.groups:
                            scoring_records.append(
                                {"team": team.uuid, "group": group.uuid, "score": None}
                            )
                    self.scoring_table = pd.DataFrame.from_dict(scoring_records)
            else:
                if self.person_level_scoring:
                    # Teams are not split into sub-groups
                    # Scoring tracked at the person level
                    scoring_records = []
                    for team in self.participants:
                        for person in team.roster:
                            scoring_records.append(
                                {"team": team.uuid, "person": person.uuid, "score": None}
                            )
                    self.scoring_table = pd.DataFrame.from_dict(scoring_records)
                else:
                    # Teams are not split into sub-groups
                    # Scoring tracked at the team level
                    scoring_records = [
                        {"team": team.uuid, "score": None} for team in self.participants
                    ]
                    self.scoring_table = pd.DataFrame.from_dict(scoring_records)
        else:
            # Event is at the individual level
            scoring_records = [
                {"person": person.uuid, "score": None} for person in self.participants
            ]
            self.scoring_table = pd.DataFrame.from_dict(scoring_records)

    def update_scores(self, new_scores: List[Dict[str, Union[int, float]]]):
        for score in new_scores:
            try:
                if isinstance(self.participants[0], Team):
                    team = score["team"]
                    if self.group_scoring:
                        group = score["group"]
                        if self.person_level_scoring:
                            person = score["person"]
                            self.scoring_table.loc[
                                (self.scoring_table["team"] == team) &
                                (self.scoring_table["group"] == group) &
                                (self.scoring_table["person"] == person),
                                "score"
                            ] = score["score"]
                        else:
                            self.scoring_table.loc[
                                (self.scoring_table["team"] == team) &
                                (self.scoring_table["group"] == group),
                                ["score"]
                            ] = score["score"]
                    else:
                        if self.person_level_scoring:
                            person = score["person"]
                            self.scoring_table.loc[
                                (self.scoring_table["team"] == team) &
                                (self.scoring_table["person"] == person),
                                ["score"]
                            ] = score["score"]
                        else:
                            self.scoring_table.loc[
                                self.scoring_table["team"] == team,
                                ["score"]
                            ] = score["score"]
                else:
                    self.scoring_table.loc[
                        self.scoring_table["person"] == person,
                        ["score"]
                    ] = score["score"]
            except Exception as e:
                print(e)
                raise AttributeError("Score provided does not match the event's configuration")

    def get_scores(self):
        if self.group_scoring:
            if self.person_level_scoring:
                group_group_obj = self.scoring_table.groupby(["team", "group"])["score"]
                team_group_obj = self.group_scoring_functions(group_group_obj).groupby(["team"])["score"]
                scores = self.team_scoring_function(team_group_obj)
            else:
                team_group_obj = self.scoring_table.groupby(["team"])["score"]
                scores = self.team_scoring_function(team_group_obj)
        else:
            if self.person_level_scoring:
                team_group_obj = self.scoring_table.groupby(["team"])["score"]
                scores = self.team_scoring_function(team_group_obj)
            else:
                scores = self.scoring_table

        return scores.to_dict()
