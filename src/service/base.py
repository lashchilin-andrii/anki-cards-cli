from abc import ABC, abstractmethod
import os
from datetime import date

from src.dictionary.base import BaseDictionary


class BaseService(ABC):
    """Base interface for word-processing services."""

    def __init__(self, dictionary: BaseDictionary):
        self.dictionary = dictionary

    @abstractmethod
    def run(self, words: list[str], path: str) -> None:
        """Run the service end-to-end."""
        raise NotImplementedError

    def save_notes(
        self,
        path: str,
        notes: list[str],
        filename_prefix: str = "words",
    ) -> None:
        """Save notes to a dated .txt file."""
        today = date.today()

        if not os.path.isdir(path):
            print(f"Directory does not exist: {path}")
            return

        final_file = os.path.join(path, f"{filename_prefix}_{today}.txt")

        try:
            with open(final_file, "w", encoding="utf-8") as f:
                for note in notes:
                    f.write(note + "\n")
            print(f"Notes saved successfully: {final_file}")
        except Exception as e:
            print(f"Failed to save notes: {e}")

    @staticmethod
    def clear_terminal() -> None:
        """Clear the terminal screen (cross-platform)."""
        os.system("cls" if os.name == "nt" else "clear")
