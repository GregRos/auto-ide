# JetBrains IDEs are tricky...
# First of all, they're all the same. They're one product, being sold multiple times. Even the config files
# don't mention the name of the IDE. But if you open a folder with the wrong IDE, you won't have all the features.
# I've found that one indication is the `module/@type` xpath in a *.iml file.

# After you try to open the IDE with a jetbrains editor that's already open, it will ask if to open that project
# in a different window, etc. That's great, but the window is out of focus. It needs to be brought into focus.
import glob
from typing import List, Sequence, TypeVar, Iterator
from loguru import logger

from .launcher import Launcher
from .bin import Bin
from .project import open_project
from ..picker import IdeManager, IdeLauncher

T = TypeVar('T')


def flatten(seqs: List[Iterator[T]]) -> Sequence[T]:
    for seq in seqs:
        yield from seq


"""Manages JB IDE configurations."""


class Manager(IdeManager):
    def __init__(self, bins: List[Bin]):
        self._bins = bins

    def _get_bin(self, key: str):
        return next(filter(lambda x: x.key == key, self._bins), None)

    def open_existing(self, path: str) -> IdeLauncher | None:
        project = open_project(path)
        if project:
            type = project.get_project_type()
            right_bin = self._get_bin(type)
            launcher = Launcher(
                path=path,
                exe=right_bin.exe,
                score=project.get_access_time() * right_bin.default_score
            )
            return launcher

    def open_new(self, path: str) -> IdeLauncher | None:
        existing = self.open_existing(path)
        if existing:
            return existing

        for bin in self._bins:
            flat = flatten([
                glob.iglob(f'{path}/{glb}') for glb in bin.globs
            ])
            for _ in flat:
                return Launcher(
                    path=path,
                    exe=bin.exe,
                    score=bin.default_score
                )
        # no files this IDE can handle
        return None
