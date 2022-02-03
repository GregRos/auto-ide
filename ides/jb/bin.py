import glob
from typing import List
from .project import ProjectType

"""A JB launch configuration."""


class Bin:
    default_score: float
    key: str
    exe: str
    globs: List[str]

    def __init__(self, key: ProjectType, exe: str, globs: List[str], default_score: float):
        self.exe = next(glob.iglob(exe))
        self.key = key
        self.globs = globs
        self.default_score = default_score
