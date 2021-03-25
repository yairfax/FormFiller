from dataclasses import dataclass
from enum import Enum

class Action:
    pass

class FieldType(Enum):
    NAME = 1
    ID = 2

@dataclass
class DataPoint:
    field: str
    value: str
    id_type: FieldType

@dataclass
class DataEntryAction(Action):
    data_points: list[DataPoint]

@dataclass
class ClickAction(Action):
    btn: str
    wait: bool

@dataclass
class SleepAction(Action):
    time: float

@dataclass
class AST:
    url: str
    actions: list[Action]