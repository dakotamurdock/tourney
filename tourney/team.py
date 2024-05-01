from typing import Dict, List, Optional, Union
from uuid import uuid1

import pandas as pd

from tourney.person import Person


class Group:
    def __init__(
        self,
        name: str,
        roster: Union[List[Person], Dict[str, Person]],
        id: str = str(uuid1())
    ):
        self.id = id
        self.name = name

        self.roster: pd.DataFrame = None
        if roster:
            if isinstance(roster[0], str):
                self.roster = pd.DataFrame(data=roster, columns=["person"])
            elif isinstance(roster[0], dict):
                self.roster = pd.DataFrame(data=roster, columns=["division", "person"])
        else:
            raise AttributeError("A roster must be provided to build a group.")
        self.roster["group"] = self


class Team:
    def __init__(
        self,
        name: str,
        id: str = str(uuid1()),
        roster: Union[List[Person], Dict[str, Person]] = None,
        groups: Optional[List[Group]] = None,
        location: Optional[str] = None,
        coaches: Optional[Union[List[Person], Dict[str, Person]]] = None
    ):
        self.id = id
        self.name = name
        self.groups = groups
        self.location = location
        self.coaches = coaches

        self.roster: pd.DataFrame = None
        if roster:
            if isinstance(roster[0], str):
                self.roster = pd.DataFrame(data=roster, columns=["person"])
            elif isinstance(roster[0], dict):
                self.roster = pd.DataFrame(data=roster, columns=["division", "person"])
        else:
            if self.groups:
                self.roster = pd.concat([group.roster for group in self.groups])
            else:
                raise AttributeError("Either a roster or a list of groups with rosters must be provided to build a team.")
        self.roster["team"] = self

        self.box_score = self.roster.copy()
        self.box_score["score"] = None
    
    def consolidate_score(self):
        scores = self.box_score.groupby([])["score"]
