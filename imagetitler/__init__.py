import tomllib

with open("pyproject.toml", "rb") as f:
    _META = tomllib.load(f)

__version__ = _META["tool"]["poetry"]["version"]
