import importlib
import os
import platform
import sys

from packaging.version import parse, Version

sys.path.append(os.path.abspath("src"))
import version
import build.base


def get_build_tool() -> build.base.BuildTool:
    ver: Version = parse(version.get_version())

    if platform.system() == "Windows":
        module = importlib.import_module("build.windows")
    elif platform.system() == "Darwin":
        module = importlib.import_module("build.macos")
    elif platform.system() == "Linux":
        module = importlib.import_module("build.linux")
    else:
        raise NotImplementedError("System is not supported")

    _build_tool = module.instance()(version=ver)
    return _build_tool