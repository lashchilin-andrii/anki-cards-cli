from abc import ABC
import os

from src.dictionary.base import BaseDictionary


class BaseService(ABC):
    """Base interface for word-processing services."""

    def __init__(self, dictionary: BaseDictionary):
        self.dictionary = dictionary

    @staticmethod
    def clear_terminal() -> None:
        """Clear the terminal screen (cross-platform)."""
        os.system("cls" if os.name == "nt" else "clear")
