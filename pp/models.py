from ast import Tuple
from datetime import datetime, timezone
from time import time
from typing import List, Literal, Union
from uuid import uuid4

from pydantic import AwareDatetime, BaseModel, Field
from typing_extensions import Annotated

from .utils import utcnow_dt


class User(BaseModel):
    id: str
    name: str
    description: str = ""


class Group(BaseModel):
    id: str
    name: str
    description: str = ""


class Role(BaseModel):
    id: str
    name: str
    description: str = ""


class EventBackend(BaseModel):
    id: str
    name: str
    description: str = ""


class StorageBackend(BaseModel):
    id: str
    name: str
    description: str = ""


class Coordinator(BaseModel):
    id: str
    name: str
    description: str = ""
    type: Literal["server", "p2p"]


class Project(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    create_at: AwareDatetime = Field(default_factory=utcnow_dt)
    name: str
    description: str = ""
    type: str = "operation_infomartion"

    def copy_to(self):
        ...

    def train(self):
        ...

    def predict(self):
        ...

    def backtest(self):
        ...

    def extract_route(self):
        ...

    def alert(self):
        ...

    def report(self):
        ...

    def query_expect(self):
        ...

    def query_actual(self):
        ...


class Schedule(BaseModel):
    name: str
    description: str = ""
    checkpoint_id: str


class ExpectSchedule(Schedule):
    ...


class ActualSchedule(Schedule):
    ...


class File(BaseModel):
    type: Literal["file"] = "file"


class URL(BaseModel):
    type: Literal["url"] = "url"


AnyIcon = Annotated[Union[File, URL], Field(discriminator="type")]


class Icon(BaseModel):
    id: str
    name: str
    description: str = ""
    params: AnyIcon


class Device(BaseModel):
    type: Literal["device"] = "device"


class Checkpoint(BaseModel):
    type: Literal["checkpoint"] = "checkpoint"


AnyEntity = Annotated[Union[Device, Checkpoint], Field(discriminator="type")]


class Entity(BaseModel):
    id: str
    name: str
    description: str = ""
    coordinates: Tuple[float, float] = [None, None]
    params: AnyEntity


class Route:
    ...


class Road(Entity, Route):
    direction: Literal["unidirectional", "bidirectional"]
    checkpoints: List[Checkpoint] = []


class RoutePlan(BaseModel, Route):
    direction: Literal["unidirectional", "bidirectional"]
    checkpoints: List[Checkpoint] = []

    def is_loop(self):
        return self.checkpoints[0] == self.checkpoints[-1]


class EventData(BaseModel):
    event_at: float
    entity_id: str
    description: str = ""
