import re
from typing import List, Iterable

import psutil
import win32con
import win32gui
import win32process
from loguru import logger

def get_processes_by_path(pth: str) -> Iterable[psutil.Process | None]:
    for proc in psutil.process_iter():
        if proc.pid > 0 and pth in proc.exe():
            yield proc
    logger.warning("No process found for {path}!", path=pth)
    return None

def find_window(exe: str, res_title=None) -> int | None:
    if res_title is None:
        res_title = ['.*']
    procs = list(get_processes_by_path(exe))
    if len(procs) == 0:
        return None
    windows = []

    def cb(hwnd, windows):
        tid, cur_pid = win32process.GetWindowThreadProcessId(hwnd)
        for proc in procs:
            if cur_pid == proc.pid:
                windows.append(hwnd)
                return

    win32gui.EnumWindows(cb, windows)
    logger.debug("For {exe} found: {windows}", exe=exe, windows=windows)
    for re_title in res_title:
        for hwnd in windows:
            print(hwnd)
            cur_title = win32gui.GetWindowText(hwnd)
            if re.match(re_title, cur_title):
                return hwnd

    return None


def maximize_window(hwnd: int) -> None:
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)


def activate_window(hwnd: int) -> None:
    logger.debug("Activate window {hwnd}", hwnd=hwnd)
    win32gui.SetForegroundWindow(hwnd)
