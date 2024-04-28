from typing import Dict, List, Optional, Union
from uuid import uuid1

from tourney.person import Person


class Group:
    def __init__(
        self,
        name: str,
        roster: Union[List[Person], Dict[str, Person]]
    ):
        self.uuid = str(uuid1())
        self.name = name
        self.roster = roster


class Team:
    def __init__(
        self,
        name: str,
        roster: Union[List[Person], Dict[str, Person]],
        groups: Optional[List[Group]] = None,
        location: Optional[str] = None,
        coaches: Optional[Union[List[Person], Dict[str, Person]]] = None
    ):
        self.uuid = str(uuid1())
        self.name = name
        self.groups = groups

        if self.groups:
            self.roster = {}
            for group in self.groups:
                self.roster[group] = group.roster
        else:
            self.roster = roster

        self.location = location
        self.coaches = coaches
