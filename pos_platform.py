from datetime import date, datetime, timezone
from time import time
from typing import List, Literal, Union
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastui import AnyComponent, FastUI, components as c, prebuilt_html
from fastui.components.display import DisplayLookup, DisplayMode
from fastui.events import BackEvent, GoToEvent
from pydantic import BaseModel, Field
from typing_extensions import Annotated


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
    create_at: datetime = Field(default_factory=lambda: datetime.fromtimestamp(time(), tz=timezone.utc))
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

    def alert(self):
        ...

    def report(self):
        ...

    def query_expect(self):
        ...

    def query_actual(self):
        ...


class Icon(BaseModel):
    id: str
    name: str
    description: str = ""
    project: Project = None


class Schedule(BaseModel):
    name: str
    description: str = ""
    checkpoint_id: str


class ExpectSchedule(Schedule):
    ...


class ActualSchedule(Schedule):
    ...


class Device(BaseModel):
    type: Literal["dog"] = "device"


class Checkpoint(BaseModel):
    type: Literal["dog"] = "checkpoint"


AnyEntity = Annotated[Union[Device, Checkpoint], Field(discriminator="type")]


class Entity(BaseModel):
    id: str
    name: str
    description: str = ""
    obj: AnyEntity


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


if __name__ == "__main__":

    class Room:
        def __init__(self, backend, me="", you=""):
            self.backend = backend
            self._me = me
            self._you = you

            self.envs = {
                "me": me,
                "you": you,
            }

        def _get_target(self, target):
            if target[:1] == "$":
                target = self.envs[target[1:]]

            if target not in self.backend:
                raise RuntimeError()

            return self.backend[target]

        def envs(self):
            return self.envs

        def me(self):
            return self._get_target(self._me)

        def you(self):
            return self._get_target(self._you)

        def get(self, target):
            return self._get_target(target)

        def where(self, target):
            return self._get_target(target)

        def diff(self, target, other):
            target = self._get_target(target)
            other = self._get_target(other)
            result = [a - b for a, b in zip(target, other)]
            return result

    world = Room(
        backend={
            "1": [1, 3],
            "2": [2, 5],
        },
        me="1",
        you="2",
    )

    while True:
        # 位置情報ベースコミュニケーション
        # 位置に関する質問コマンドを実装
        # 他はチャット同じ感じにしたい
        command = input("$")
        cmd, _, args = command.partition(" ")
        if not cmd:
            continue

        try:
            method = getattr(world, cmd)
            args = [x for x in args.split(" ") if x]
            result = method(*args)
            print(result)
        except Exception as e:
            print(f'["ERROR"]{e}')
