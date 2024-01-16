import packaging.version

__VERSION = "1.0"


def get_version(parsed: bool = False) -> packaging.version.Version | str:
    if parsed:
        return packaging.version.parse(__VERSION)
    else:
        return __VERSION
