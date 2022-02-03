import glob
import os
import subprocess
from loguru import logger

import fsutil

# vscode is easy to detect... just check for the .vscode folder
from ides import IdeManager, IdeLauncher

"""The vscode project launcher."""


class Launcher(IdeLauncher):
    name = "VsExecutor"
    exe: str
    path: str
    score: float

    def __init__(self, exe, path, score: float):
        self.float = score
        self.exe = exe
        self.path = path
        self.score = score

    def launch(self):
        logger.info('Going to run: "{exe}" "{path}"', exe=self.exe, path=self.path)
        subprocess.Popen([self.exe, self.path])
        return True


def score_by_atime(path: str):
    return max([os.stat(x).st_atime for x in glob.glob(f'{path}/.vscode/*')])


"""The vscode launch manager."""


class Manager(IdeManager):
    default_score: float
    location: str

    def __init__(self, location: str, default_score: float):
        self.default_score = default_score
        self.location = location

    def open_existing(self, path: str):
        logger.debug('Trying to open existing: "{path}"', path=path)
        test_path = f'{path}/.vscode'
        if fsutil.exists(test_path):
            return Launcher(self.location, path, score_by_atime(path))

    def open_new(self, path: str):
        logger.debug("Trying to open new: {path}", path=path)
        existing = self.open_existing(path)
        if existing:
            return existing
        return Launcher(
            exe=self.location,
            score=self.default_score,
            path=path
        )
