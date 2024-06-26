import random
import string

import pandas as pd
import numpy as np
from faker import Faker

from tourney.competition import Competition
from tourney.event import Event
from tourney.person import Person
from tourney.scoring import sum_scores
from tourney.team import Team, Group

# Set print configs
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Create a Faker instance
fake = Faker()


def test_person():
    """Test instantiation of Person class and attribute consistency"""
    test_name = fake.name()
    test_birthdate = fake.date()
    test_gender = random.choice(["male", "female", "transgender"])
    test_height = np.random.randint(low=60, high=79)
    test_weight = np.random.randint(low=105, high=247)

    test_person = Person(
        name=test_name,
        birthdate=test_birthdate,
        gender=test_gender,
        height=test_height,
        weight=test_weight
    )

    assert isinstance(test_person, Person)
    assert test_person.name == test_name
    assert test_person.birthdate == test_birthdate
    assert test_person.gender == test_gender
    assert test_person.height == test_height
    assert test_person.weight == test_weight


def test_group():
    divisions = ["A", "B"]
    test_roster = [{"division": random.choice(divisions), "person": Person(name=fake.name())} for _ in range(20)]

    test_name_a = fake.company()
    test_name_b = fake.company()
    test_name_c = fake.company()
    test_name_d = fake.company()
 
    group_a = Group(
        name=test_name_a,
        roster=test_roster[0:5]
    )
    group_b = Group(
        name=test_name_b,
        roster=test_roster[5:10]
    )
    group_c = Group(
        name=test_name_c,
        roster=test_roster[10:15]
    )
    group_d = Group(
        name=test_name_d,
        roster=test_roster[15:20]
    )

    assert group_a.name == test_name_a
    assert group_b.name == test_name_b
    assert group_c.name == test_name_c
    assert group_d.name == test_name_d

    assert group_a.roster.shape == (5, 3)
    assert group_b.roster.shape == (5, 3)
    assert group_c.roster.shape == (5, 3)
    assert group_d.roster.shape == (5, 3)

    test_team_name_a = fake.company()
    test_team_name_b = fake.company()

    test_location_a = fake.city()
    test_location_b = fake.city()

    test_team_a = Team(
        name=test_team_name_a,
        groups=[group_a, group_c],
        location=test_location_a
    )

    test_team_b = Team(
        name=test_team_name_b,
        groups=[group_b, group_d],
        location=test_location_b
    )

    print(test_team_a.roster)
    print(test_team_a.box_score)

    raise AttributeError




# def test_create_team():

#     test_name = fake.company()
#     test_roster = {random.choice(string.ascii_letters): Person(name=fake.name()) for _ in range(15)}
#     test_coaches = {random.choice(string.ascii_letters): fake.name() for _ in range(3)}
#     test_location = fake.city()

#     test_team = Team(
#         name=test_name,
#         roster=test_roster,
#         location=test_location,
#         coaches=test_coaches
#     )

#     # test object attributes
#     assert test_team.name == test_name
#     assert test_team.roster == test_roster
#     assert test_team.location == test_location
#     assert test_team.coaches == test_coaches


# def test_create_competition_w_two_halves():
#     # Create Teams that will compete
#     team_a = Team(
#         name="A Team",
#         roster=[Person(name=fake.name()) for _ in range(10)],
#     )
#     team_b = Team(
#         name="B Team",
#         roster=[Person(name=fake.name()) for _ in range(10)],
#     )
#     teams = [team_a, team_b]

#     # Set up Events of the competition
#     start_time = fake.date_time(),
#     first_half = Event(
#         name="1st Half",
#         participants=[team_a, team_b],
#         team_scoring_function=sum_scores,
#         person_level_scoring=True,
#         duration=30,
#         duration_unit="min",
#         scoring_unit="points"
#     )
#     second_half = Event(
#         name="2nd Half",
#         participants=[team_a, team_b],
#         duration=30,
#         duration_unit="min",
#         scoring_unit="points"
#     )

#     assert isinstance(first_half.scoring_table, pd.DataFrame)

#     score_sim = []
#     for team in teams:
#         for person in team.roster:
#             score_sim.append(
#                 {"team": team.uuid, "person": person.uuid, "score": random.randint(0, 15)}
#             )

#     first_half.update_scores(new_scores=score_sim)
#     print(first_half.get_scores())
#     raise AssertionError
#     # second_half.update_scores(new_scores={team_a: 26, team_b: 23})

#     # for test_cumulative_scoring_method in IterableCumulativeScoringMethods:
#     #     # Set up Competition
#     #     game = Competition(
#     #         name="Game 1",
#     #         cumulative_scoring_method=test_cumulative_scoring_method,
#     #         datetime_start=start_time,
#     #         events=[first_half, second_half],
#     #         event_graph={
#     #             first_half: [second_half]
#     #         }
#     #     )

#     #     assert [participant.name for participant in game.participants].sort() == ["A Team", "B Team"].sort()
#     #     final_score = game.get_score()

#     #     if test_cumulative_scoring_method == "sum":
#     #         assert final_score[team_a] == 48
#     #         assert final_score[team_b] == 47
#     #     elif test_cumulative_scoring_method == "mean":
#     #         assert final_score[team_a] == 24
#     #         assert final_score[team_b] == 23.5
#     #     elif test_cumulative_scoring_method == "max":
#     #         assert final_score[team_a] == 26
#     #         assert final_score[team_b] == 24
#     #     elif test_cumulative_scoring_method == "min":
#     #         assert final_score[team_a] == 22
#     #         assert final_score[team_b] == 23

