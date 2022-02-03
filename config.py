from ides.jb import Manager as JbManager, Bin as JbBin
from ides import IdeManager as Manager, SuperManager
from ides.vscode import Manager as VsCode

# This will first try to find project metadata...
# If it fails, it will try to run the globs and see if they match.
# VsCode can match any folder and has no globs, but has a low score
_jb = JbManager([
    JbBin(
        key='web',
        exe=r'C:\Program Files\JetBrains\PhpStorm*\bin\phpstorm64.exe',
        globs=[
            "node_modules",
            "package.json",
            "package-lock.json",
            "tsconfig.json",
            "bitbucket-pipelines.yml"
        ],
        default_score=1
    ),
    JbBin(
        key='python',
        exe=r'C:\Program Files\JetBrains\PyCharm*\bin\pycharm64.exe',
        globs=[
            "*.py"
        ],
        default_score=2
    ),
    JbBin(
        key='cpp',
        exe=r'C:\Program Files\JetBrains\CLion*\bin\clion64.exe',
        globs=[
            "Makefile",
            "*clang*",
            "*.v8",
            "*.c",
            "*.cpp"
        ],
        default_score=3
    )
])

_vscode = VsCode(
    r'C:\Users\GregRosenbaum\AppData\Local\Programs\Microsoft VS Code\Code.exe',
    0
)

manager = SuperManager(
    _jb,
    _vscode
)
