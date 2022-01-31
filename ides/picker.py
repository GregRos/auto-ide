import subprocess
import sys
import typing
from abc import abstractmethod

class IdeExecutor(typing.Protocol):
    path: str
    exe: str
    score: float
    name: str
    @abstractmethod
    def exec(self) -> bool: pass

class IdeLauncher(typing.Protocol):
    @abstractmethod
    def get(self, path: str) -> IdeExecutor | None: pass

class IdePicker:
    _ides: typing.List[IdeLauncher]

    def __init__(self, ides: typing.List[IdeLauncher]):
        self._ides = ides

    def get_ide(self, path: str) -> IdeExecutor | None:
        all_execs = [
             exec for exec in [
                ide.get(path) for ide in self._ides
            ] if exec
        ]
        print(all_execs)
        highest=max(all_execs, key=lambda x: x.score)
        return highest

