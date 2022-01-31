import argparse
import sys
from os import chdir
from os.path import dirname

from ides.jb import JbIde
from ides.vscode import VsCodeIde
from ides.picker import IdePicker

ides = IdePicker([
    JbIde({
        'WEB_MODULE': r'C:\Program Files\JetBrains\PhpStorm*\bin\phpstorm64.exe',
        'PYTHON_MODULE': r'C:\Program Files\JetBrains\PyCharm*\bin\pycharm64.exe',
        'CPP_MODULE': r'C:\Program Files\JetBrains\CLion*\bin\clion64.exe'
    }),
    VsCodeIde(r'C:\Users\GregRosenbaum\AppData\Local\Programs\Microsoft VS Code\Code.exe')
])

root_parser = argparse.ArgumentParser(description='spotify automation script')
root_parser.add_argument("path", type=str)
chdir(dirname(__file__))

if __name__ == '__main__':
    path = root_parser.parse_args().path
    ide = ides.get_ide(path)
    if not ide:
        print(f'AutoIDE - IDE not found for path "{path}".', file=sys.stderr)
        exit(1)

    try:
        ide.exec()
    except Exception as e:
        print(f'AutoIDE Error - {e.args}')




