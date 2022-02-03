import re
import subprocess
import time

from win32com import client as comclt
from loguru import logger

from automation import windows
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

    def _find_own_window(self):
        print(f'find own window: {self._path}')
        return windows.find_window(self._exe, [f'.*{re.escape(self._path)}'])

    def _had_window(self):
        return windows.find_window(self._exe)

    def launch(self):
        # Running JB behaves erratically based on
        had_window = self._had_window()
        old_project_window = self._find_own_window()

        subprocess.Popen([self._exe, self._path])
        if not had_window:
            logger.info("Didn't have own window. Process started from scratch.")
            print(f'JB - no previous window: {self._exe}')
            time.sleep(2.5)
            new_window = self._find_own_window()
            if not new_window:
                return
            windows.activate_window(new_window)
            windows.maximize_window(new_window)
            # If there was no previous window for this IDE, this was enough
            return
        elif old_project_window is not None:
            logger.info("Project window already existed.")
            print(f'JB - had project window: {self._exe} hwnd {old_project_window}')
            windows.maximize_window(old_project_window)
            return
        time.sleep(0.4)

        # Sometimes creates a new window called 'Open Project' other times it just
        # appears in the normal window
        choice_window = windows.find_window(self._exe, [r'^Open Project.*', r'^\w+ \[.*', r'^\w+ -.*'])
        if not choice_window:
            raise Exception('Choice window not found.')

        logger.info("GUI window found.", hwnd=choice_window)
        windows.activate_window(choice_window)
        logger.info("activated")
        time.sleep(0.3)
        wsh = comclt.Dispatch("WScript.Shell")
        wsh.SendKeys("%w")
        time.sleep(0.5)
        logger.info("GUI automated")
        ide_window = windows.find_window(self._exe, [f'.*{re.escape(self._path)}'])
        if not ide_window:
            raise Exception('IDE window not found.')
        logger.info("Project window found and opened.")
        windows.activate_window(ide_window)
        windows.maximize_window(ide_window)
