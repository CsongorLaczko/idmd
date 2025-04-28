from importlib.metadata import PackageNotFoundError, version

from .app import DataApp
from .data.export import DataExporter
from .data.loader import FileUploader
from .ui.column_manipulator import ColumnManipulator
from .ui.data_stats import DataStats
from .viz.visualizer import DataVisualizer

__all__ = [
    "DataApp",
    "FileUploader",
    "DataStats",
    "ColumnManipulator",
    "DataVisualizer",
    "DataExporter",
]

try:
    __version__ = version("idmd")
except PackageNotFoundError:
    __version__ = "0.0"
