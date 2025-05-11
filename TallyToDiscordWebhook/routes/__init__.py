import os
from pathlib import Path

CURRENT_FILE = Path(__file__)
CURRENT_PARENT = CURRENT_FILE.parent
ROOT_DIRECTORY = Path(os.path.realpath(__file__)).parent.parent.parent

module: Path
for module in CURRENT_PARENT.iterdir():
    if not module.suffix == '.py' or '__init__.py' in str(module):
        continue

    package = str(module.relative_to(ROOT_DIRECTORY)).replace('/', '.').removesuffix('.py')
    exec(f'from {package} import *')
