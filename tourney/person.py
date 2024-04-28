from datetime import date
from typing import Optional
from uuid import uuid1


class Person:
    def __init__(
        self,
        name: Optional[str],
        birthdate: Optional[date] = None,
        gender: Optional[str] = None,
        height: Optional[float] = None,
        weight: Optional[float] = None,
    ):
        self.uuid = str(uuid1())
        self.name = name
        self.birthdate = birthdate
        self.gender = gender
        self.height = height
        self.weight = weight
