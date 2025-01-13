from __future__ import annotations

import importlib
from typing import Any


def import_module_from_str(string_path: str) -> Any:
    paths = string_path.split(".")
    if len(paths) == 3:
        module = importlib.import_module(f"{paths[0]}.{paths[1]}")
        return getattr(module, paths[2])
    elif len(paths) == 2:
        module = importlib.import_module(f"{paths[0]}")
        return getattr(module, paths[1])
    try:
        module = importlib.import_module(f"{string_path}")
    except Exception as e:
        raise Exception(f"Failed to import {string_path} with \n:{e}")
    return module
