from abc import ABC, abstractmethod


class BaseDictionary(ABC):
    """Abstract base class for all dictionaries."""

    name: str

    @abstractmethod
    def get_entry(self, word: str) -> list:
        """Return a list of objects for the given word."""
        raise NotImplementedError
