from abc import ABC, abstractmethod
from backend.model.entry import Entry


class BaseDictionary(ABC):
    """Abstract base class for all dictionaries."""

    name: str

    @abstractmethod
    def get_entry(self, word: str) -> list[Entry]:
        """Return a list of Entry objects for the given word."""
        raise NotImplementedError
