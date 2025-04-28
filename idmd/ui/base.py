# idmd/ui/base.py
from abc import ABC, abstractmethod


class Component(ABC):
    """Abstract base class for all UI components"""

    @abstractmethod
    def render(self) -> None:
        """Render component in Streamlit interface"""
        raise NotImplementedError

    @property
    def position(self) -> str:
        """Determine component column placement"""
        return "left"
