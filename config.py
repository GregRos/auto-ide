from ides.jb import Manager as JbManager, Bin as JbBin
from ides import IdeManager as Manager, SuperManager
from ides.vscode import Manager as VsCode

# This will first try to find project metadata...
# If it fails, it will try to run the globs and see if they match.
# VsCode can match any folder and has no globs, but has a low score
_jb = JbManager([
    JbBin(
        key='web',
        exe=r'/home/gr/grwsl/apps/phpstorm',
        globs=[
            "node_modules",
            "package.json",
            "package-lock.json",
            "tsconfig.json",
            "bitbucket-pipelines.yml"
        ],
        default_score=1.01
    ),
    JbBin(
        key='python',
        exe=r'/home/gr/grwsl/apps/pycharm',
        globs=[
            "*.py"
        ],
        default_score=2
    )
])

_vscode = VsCode(
    r'/usr/bin/code',
    1
)

manager = SuperManager(
    _jb,
    _vscode
)
