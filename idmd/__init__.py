from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("idmd")
except PackageNotFoundError:
    __version__ = "0.0"
