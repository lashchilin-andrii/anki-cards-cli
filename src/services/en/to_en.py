from questionary import checkbox
from src.services.base import BaseService
from src.models.entry import Entry


class EnToEnService(BaseService):
    """English-to-English note-taking service using any dictionary."""

    # ---------- DICTIONARY ----------

    def get_word_entries(self, word: str) -> list[Entry]:
        """Fetch word entries (definitions + examples) from the injected dictionary."""
        word = word.strip()
        if not word:
            return []

        entries = self.dictionary.get_entry(word)
        if not entries:
            print(f"[{self.dictionary.name}] Word '{word}' not found. Skipping.\n")
        return entries

    # ---------- USER SELECTION ----------

    def select_definitions(self, entries: list[Entry]) -> list[Entry]:
        """Let the user select definitions for a word."""
        if not entries:
            return []

        selected_defs = checkbox(
            f"SELECT DEFINITIONS FOR '{entries[0].spelling.upper()}'",
            choices=[e.definition for e in entries],
            instruction="",
        ).ask()

        if not selected_defs:
            return []

        return [e for e in entries if e.definition in selected_defs]

    def select_examples(self, entry: Entry) -> Entry:
        """Let the user select examples for a given entry."""
        if entry.examples:
            selected_examples = checkbox(
                f"'{entry.spelling.upper()}' — {entry.definition.upper()}",
                choices=entry.examples,
                instruction="",
            ).ask()
            entry.examples = selected_examples or []
        else:
            entry.examples = []
        return entry

    # ---------- PIPELINE ----------

    def process_words(self, words: list[str]) -> list[str]:
        """Fetch, filter, and convert words to string notes."""
        all_notes: list[str] = []

        for word in words:
            entries = self.get_word_entries(word)
            if not entries:
                continue

            selected_entries = self.select_definitions(entries)
            if not selected_entries:
                continue

            for entry in selected_entries:
                entry = self.select_examples(entry)
                all_notes.append(str(entry))

            self.clear_terminal()

        return all_notes

    def run(self, words: list[str], path: str) -> None:
        """Main workflow: process words and save as txt file."""
        notes = self.process_words(words)

        if not notes:
            print("No notes were created. Exiting.")
            return

        self.save_notes(path, notes)
