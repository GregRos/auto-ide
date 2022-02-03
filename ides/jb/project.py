import glob
import logging
import os
from typing import TypeAlias, Literal
from xml.etree import ElementTree
from loguru import logger

import fsutil

ProjectType: TypeAlias = Literal["web", "python", "cpp"]
"""A JB project."""


class Project:
    _path: str

    def __init__(self, path: str):
        self._path = path

    def _get_iml_file(self) -> str | None:
        results = self.glob("*.iml")
        if len(results) >= 1:
            [only] = results
            return only

    def _get_module_type(self) -> str | None:
        file = self._get_iml_file()
        if file:
            x = ElementTree.parse(file)
            e_module = x.getroot()
            return e_module.get('type')

    def get_project_type(self) -> ProjectType:
        match self._get_module_type():
            case 'WEB_MODULE':
                return 'web'
            case 'CPP_MODULE':
                return 'cpp'
            case 'PYTHON_MODULE':
                return 'python'
            case other:
                logger.error('Unknown module type %s', other)
                raise Exception(f'Unknown module type {other}')

    def glob(self, p: str):
        return glob.glob(f'{self._path}/{p}')

    def get_access_time(self) -> float:
        results = self.glob(f'*.xml')
        max_access = max([os.stat(file).st_atime for file in results])
        logger.error('Access time %f', max_access)
        return max_access


def open_project(path: str):
    jb_folder = f'{path}/.idea'
    if fsutil.exists(jb_folder):
        return Project(jb_folder)
