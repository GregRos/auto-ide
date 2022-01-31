import glob
import os
import subprocess

import fsutil

# vscode is easy to detect... just check for the .vscode folder
class VsCodeIde:
    class Executor:
        name = "VsExecutor"
        exe: str
        path: str
        score: float
        def __init__(self, exe, path):
            self.exe = exe
            self.path = path
            self.score = max([os.stat(x).st_atime for x in glob.glob(f'{path}/.vscode/*')])

        def exec(self):
            subprocess.Popen([self.exe, self.path])
            return True

    location: str
    def __init__(self, location):
        self.location = location

    def get(self, path):
        testPath = f'{path}/.vscode'
        if fsutil.exists(testPath):
            return self.Executor(self.location, path)
