from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("idmd")
except PackageNotFoundError:
    __version__ = "0.0"