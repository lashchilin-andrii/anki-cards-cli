from src.services import base
from src.models.word_entry import WordEntry
from src.dictionaries import cambridge_dict
from questionary import checkbox


def get_word_entries(word: str) -> list[WordEntry]:
    """Fetch word entries (definitions + examples) from dictionary."""
    word = word.strip()
    if not word:
        return []

    entries: list[WordEntry] = cambridge_dict.get_word_entry(word)
    if not entries:
        print(f"Word '{word}' not found. Skipping.\n")
    return entries


def select_definitions(entries: list[WordEntry]) -> list[WordEntry]:
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


def select_examples(entry: WordEntry) -> WordEntry:
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


def process_words(words: list[str]) -> list[str]:
    """Fetch, filter, and convert words to string notes."""
    all_notes = []

    for word in words:
        entries = get_word_entries(word)
        if not entries:
            continue

        selected_entries = select_definitions(entries)
        if not selected_entries:
            continue

        for entry in selected_entries:
            entry = select_examples(entry)
            all_notes.append(str(entry))

        base.clear_terminal()

    return all_notes


def run(words: list[str], path: str):
    """Main workflow: process words and save as txt file."""
    notes = process_words(words)

    if not notes:
        print("No notes were created. Exiting.")
        return

    base.save_notes(path, notes)
    print(f"[INFO] Notes saved successfully to {path}")
