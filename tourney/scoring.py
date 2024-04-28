from typing import Dict, Union

import numpy as np
import pandas as pd
from numpy import array
from scipy.stats import rankdata

from tourney.team import Team
from tourney.person import Person


def rank_scores(scores: Dict[Union[Team, Person], Union[int, float]], rank_method: str="min", better: str="low") -> Dict[Union[Team, Person], int]:
    score_keys = list(scores.keys())
    score_values = array(list(scores.values()))

    if better == "high":
        score_values = -score_values

    score_ranks = rankdata(a=score_values, method=rank_method)

    ranks = {}
    ranks.update(zip(score_keys, score_ranks))

    return ranks


def sum_scores(grouped_obj):
    return grouped_obj.sum()


def min_scores(grouped_obj):
    return grouped_obj.min()


def max_scores(grouped_obj):
    return grouped_obj.max()


def mean_scores(grouped_obj):
    return grouped_obj.mean()


def median_scores(grouped_obj):
    return grouped_obj.median()


def best_n_scores(
        scores: Dict[Union[Team, Person], Union[int, float]],
        best_n: int = 1,
        rank_method: str = "min", 
        better: str = "low"
    ):
    score_keys = list(scores.keys())
    score_values = list(scores.values())
    all_scores = pd.DataFrame({"entity": score_keys, "score": score_values})

    ascending = True
    if better == "high":
        ascending = False

    all_scores["rank"] = all_scores["score"].rank(method=rank_method, ascending=ascending)
    all_scores.sort_values(by="rank", inplace=True)

    top_scores = all_scores.head(best_n)
    
    final_scores = {top_scores.iloc[idx]["entity"]: top_scores.iloc[idx]["score"] for idx in range(top_scores.shape[0])}
    
    return final_scores


if __name__ == "__main__":
    scores = {"test_1": 23, "test_2": 24, "test_3": 17, "test_4": 32, "test_5": 20}
    print(best_n_scores(scores, better="high", best_n=3))
