import ast
import os
import sys
from pathlib import Path
from types import ModuleType
from unittest.mock import MagicMock

import numpy as np

from tests.constants import CURRENT_OS

_MAIN_PATH = Path(__file__).resolve().parent.parent / "__main__.py"


def load_main():
    source = _MAIN_PATH.read_text()
    tree = ast.parse(source, filename=str(_MAIN_PATH))

    keep_nodes = []
    for node in tree.body:
        if isinstance(node, ast.If):
            try:
                if (
                    hasattr(node.test, "comparators")
                    and hasattr(node.test, "left")
                    and hasattr(node.test.left, "id")
                    and node.test.left.id == "__name__"
                ):
                    continue
            except AttributeError:
                pass
        if hasattr(node, "lineno") and node.lineno >= 257:
            break
        keep_nodes.append(node)

    mock_me = ModuleType("me")
    mock_me.generate_header = lambda: "HEADER"
    sys.modules["me"] = mock_me

    mod = ModuleType("test_main")
    mod.__file__ = str(_MAIN_PATH)

    mock_os = MagicMock()
    mock_os.get_terminal_size.return_value = os.terminal_size((80, 24))
    mod.__dict__["os"] = mock_os
    mod.__dict__["sys"] = sys

    mock_platform = MagicMock()
    mock_platform.system.return_value = CURRENT_OS
    mod.__dict__["platform"] = mock_platform

    mock_time = MagicMock()
    mock_time.sleep = MagicMock()
    mod.__dict__["time"] = mock_time

    import random as _random

    mod.__dict__["random"] = _random
    mod.__dict__["np"] = np

    from dataclasses import dataclass

    mod.__dict__["dataclass"] = dataclass

    mod_body = ast.Module(body=keep_nodes, type_ignores=[])
    ast.fix_missing_locations(mod_body)
    code = compile(mod_body, str(_MAIN_PATH), "exec")
    exec(code, mod.__dict__)

    mod.__dict__["platform"] = mock_platform

    if "me" in sys.modules:
        del sys.modules["me"]

    return mod
