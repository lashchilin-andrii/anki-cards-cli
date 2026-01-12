from backend.dictionary.base_service import BaseService
from backend.dictionary.en.en.cambridge.model import Entry
import os
from datetime import date


class CambridgeDictionaryService(BaseService):
    """Cambridge Dictionary service."""

    def get_entry(self, word: str) -> list[Entry]:
        """Return the entry for a word."""
        if not word:
            return []
        return self.dictionary.get_entry(word)

    def save_entries_txt(
        self,
        path: str,
        entries: list[str],
    ) -> None:
        """Save entries to a .txt file."""
        if not os.path.isdir(path):
            print(f"Directory does not exist: {path}")
            return

        final_file = os.path.join(path, f"words_{date.today()}.txt")

        try:
            with open(final_file, "w", encoding="utf-8") as f:
                for entry in entries:
                    f.write(entry + "\n")
            print(f"Notes saved successfully: {final_file}")
        except Exception as e:
            print(f"Failed to save notes: {e}")
