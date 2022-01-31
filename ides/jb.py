# JetBrains IDEs are tricky...
# First of all, they're all the same. They're one product, being sold multiple times. Even the config files
# don't mention the name of the IDE. But if you open a folder with the wrong IDE, you won't have all the features.
# I've found that one indication is the `module/@type` xpath in a *.iml file.

# After you try to open the IDE with a jetbrains editor that's already open, it will ask if to open that project
# in a different window, etc. That's great, but the window is out of focus. It needs to be brought into focus.
import glob
import os
import re
import subprocess
import sys
import time
import win32com.client as comclt
import functools
from os import stat_result
from xml.etree import ElementTree

import fsutil

from ides import windows

class JbIde:
    class Executor:
        path: str
        exe: str
        score: float
        name = "JbExecutor"
        def _get_access_time(self, path: str) -> float:
            def access_time(file: str):
                return os.stat(file).st_atime
            results = glob.glob(f'{path}/.idea/*.xml')
            max_access = max([os.stat(file).st_atime for file in results])
            return max_access

        def __init__(self, path: str, exe: str):
            self.path = path
            self.exe = exe
            self.score = self._get_access_time(path)

        def find_own_window(self):
            print(f'find own window: {self.path}')
            return windows.find_window(self.exe, [f'.*{re.escape(self.path)}'])

        def had_window(self):
            return windows.find_window(self.exe) is not None

        def exec(self):
            had_window = self.had_window()
            old_project_window = self.find_own_window()

            subprocess.Popen([self.exe, self.path])
            if not had_window:
                print(f'JB - no previous window: {self.exe}')
                time.sleep(2.5)
                new_window = self.find_own_window()
                if not new_window:
                    return
                windows.activate_window(new_window)
                windows.maximize_window(new_window)
                # If there was no previous window for this IDE, this was enough
                return
            elif old_project_window is not None:
                print(f'JB - had project window: {self.exe} hwnd {old_project_window}')
                windows.maximize_window(old_project_window)
                return
            time.sleep(0.4)

            # Sometimes creates a new window called 'Open Project' other times it just
            # appears in the normal window
            choice_window = windows.find_window(self.exe, [r'^Open Project.*', r'^\w+ \[.*', r'^\w+ -.*'])
            if not choice_window:
                raise Exception('Choice window not found.')

            print(f'window found: {choice_window}')
            windows.activate_window(choice_window)
            time.sleep(0.3)
            wsh = comclt.Dispatch("WScript.Shell")
            wsh.SendKeys("%w")
            time.sleep(0.5)
            ide_window = windows.find_window(self.exe, [f'.*{re.escape(self.path)}'])
            if not ide_window:
                raise Exception('IDE window not found.')
            windows.activate_window(ide_window)
            windows.maximize_window(ide_window)


    def __init__(self, module_to_path: dict):
        self._paths = module_to_path

    def _get_xml_file(self, path: str) -> str | None:
        results = glob.glob(f'{path}/.idea/*.iml')
        if len(results) >= 1:
            [only] = results
            return only

    def _get_module_type(self, path: str) -> str | None:
        file = self._get_xml_file(path)
        if file:
            x = ElementTree.parse(file)
            rt = x.getroot()
            e_module = x.getroot()
            return e_module.get('type')

    def _match(self, path: str) -> str | None:
        type = self._get_module_type(path)
        if type:
            ide = self._paths.get(type)
            [ideExe] = glob.glob(ide)
            return ideExe

    def get(self, path: str):
        exe = self._match(path)
        if exe:
            return self.Executor(path, exe)
