from backend.service.base import BaseService
from backend.model.entry import Entry
import os
from datetime import date


class EnToEnService(BaseService):
    """English-to-English note-taking service using any dictionary."""

    def get_word_entries(self, word: str) -> list[Entry]:
        """Return all entries for a word."""
        word = word.strip()
        if not word:
            return []
        return self.dictionary.get_entry(word)

    def get_notes_as_strings_from_entries(
        self,
        selections: dict[str, list[Entry]],
    ) -> list[str]:
        """Convert selected entries into note strings."""
        notes: list[str] = []

        for word, entries in selections.items():
            for entry in entries:
                notes.append(str(entry))

        return notes

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

    def save_notes_to_path(self, notes: list[str], path: str):
        self.save_notes(path, notes)
