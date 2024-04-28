import typing
from datetime import datetime
from statistics import mean, median, mode
from typing import Dict, List, Literal, Optional, Union

import networkx as nx

from tourney.event import Event
from tourney.team import Team
from tourney.person import Person
from tourney.utils import CumulativeScoringMethods


class Competition:
    def __init__(
        self, 
        name: str,
        events: List[Event],
        cumulative_scoring_method: CumulativeScoringMethods,
        datetime_start: Optional[datetime] = None,
        datetime_end: Optional[datetime] = None
    ):
        self.name = name
        self.events = events
        self.cumulative_scoring_method = cumulative_scoring_method
        self.datetime_start = datetime_start
        self.datetime_end = datetime_end

        # Set up graph of events
        self.event_graph = nx.DiGraph().add_nodes_from(self.events)

        # Set participants competing
        participants = set()
        for event in self.events:
            for participant in event.participants:
                participants.add(participant)
        self.participants = list(participants)

        # Initialize Score
        self.scores = {participant: None for participant in self.participants}

    def connect_events(self, event_from: Event, event_to: Event):
        self.event_graph.add_edge(event_from, event_to)

    def get_score(self):
        for participant in self.participants:
            if self.cumulative_scoring_method == "sum":
                self.scores[participant] = sum([event.scores[participant] for event in self.events])
            elif self.cumulative_scoring_method == "mean":
                self.scores[participant] = mean([event.scores[participant] for event in self.events])
            elif self.cumulative_scoring_method == "median":
                self.scores[participant] = median([event.scores[participant] for event in self.events])
            elif self.cumulative_scoring_method == "mode":
                self.scores[participant] = mode([event.scores[participant] for event in self.events])
            elif self.cumulative_scoring_method == "max":
                self.scores[participant] = max([event.scores[participant] for event in self.events])
            elif self.cumulative_scoring_method == "min":
                self.scores[participant] = min([event.scores[participant] for event in self.events])
        
        return self.scores
