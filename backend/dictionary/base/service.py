from abc import ABC, abstractmethod
import os

from backend.dictionary.base.dictionary import BaseDictionary


class BaseService(ABC):
    """Base interface for word-processing services."""

    def __init__(self, dictionary: BaseDictionary):
        self.dictionary = dictionary

    @abstractmethod
    def get_entry(self, word: str) -> list:
        """Return the entry for a word."""
        raise NotImplementedError

    @abstractmethod
    def save_entries_txt(self, path: str, entries: list) -> None:
        """Save entries to a .txt file."""
        raise NotImplementedError

    @staticmethod
    def clear_terminal() -> None:
        """Clear the terminal screen (cross-platform)."""
        os.system("cls" if os.name == "nt" else "clear")
