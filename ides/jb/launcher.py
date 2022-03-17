import re
import subprocess
import time

from loguru import logger
from .. import IdeLauncher

"""The JB project launcher."""


class Launcher(IdeLauncher):
    _path: str
    _exe: str
    score: float
    name = "JbExecutor"

    def __init__(self, path: str, exe: str, score: float):
        self._path = path
        self._exe = exe
        self.score = score

    def launch(self):
        p = subprocess.Popen([self._exe, self._path])
        try:
            code = p.wait()
        except subprocess.TimeoutExpired:
            return True
        
