import subprocess
import sys
import typing
from abc import abstractmethod

"""Launches IDEs."""


class IdeLauncher(typing.Protocol):
    path: str
    exe: str
    score: float
    name: str

    @abstractmethod
    def launch(self) -> bool: pass


"""Manages IDE launchers."""


class IdeManager(typing.Protocol):
    @abstractmethod
    def open_existing(self, path: str) -> IdeLauncher | None: pass

    def open_new(self, path: str) -> IdeLauncher | None: pass


"""Manages launch managers"""


class SuperManager:
    _ides: typing.List[IdeManager]
    _default: str

    def __init__(self, *ides: IdeManager):
        self._ides = list(ides)

    def _try_existing(self, path: str):
        launchers = [
            launcher for launcher in [
                ide.open_existing(path) for ide in self._ides
            ] if launcher
        ]
        print(launchers)
        if len(launchers) > 0:
            # return the best IDE by score
            highest = max(launchers, key=lambda x: x.score)
            return highest

    def _open_new(self, path: str):
        launchers = [
            launcher for launcher in [
                ide.open_new(path) for ide in self._ides
            ] if launcher
        ]
        return max(launchers, key=lambda x: x.score)

    def get_ide(self, path: str) -> IdeLauncher | None:
        existing = self._try_existing(path)
        if existing:
            return existing

        return self._open_new(path)
