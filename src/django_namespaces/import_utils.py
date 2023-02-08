
import importlib


def import_module_from_str(string_path):
    paths = string_path.split('.')
    if len(paths) == 3:
        module = importlib.import_module(f"{paths[0]}.{paths[1]}")
        return getattr(module, paths[2])
    elif len(paths) == 2:
        module = importlib.import_module(f"{paths[0]}")
        return getattr(module, paths[1])
    else:
        try:
            module = importlib.import_module(f"{string_path}")
        except Exception as E:
            raise f"Failed to import {string_path} with \n:{E}"
    return module