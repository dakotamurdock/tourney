import typing

CumulativeScoringMethods = typing.Literal[
    "sum",
    "mean",
    "median",
    "mode",
    "max",
    "min"
]

IterableCumulativeScoringMethods = typing.get_args(CumulativeScoringMethods)
