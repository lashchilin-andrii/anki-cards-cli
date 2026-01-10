import argparse
from questionary import checkbox

from backend.service import create_service
from backend.service.en.en import EnToEnService
from backend.model.entry import Entry

def parse_args():
    parser = argparse.ArgumentParser(description="Create simple Anki-style word cards.")

    parser.add_argument("words", nargs="+", help="List of words separated by spaces.")
    parser.add_argument("-p", "--path", required=True, help="Path to save the file.")
    parser.add_argument(
        "-f",
        "--from",
        dest="source",
        default="en",
        type=str.lower,
        help="Source language code.",
    )
    parser.add_argument(
        "-t",
        "--to",
        dest="target",
        default="en",
        type=str.lower,
        help="Target language code.",
    )
    parser.add_argument(
        "-d",
        "--dictionary",
        default="cambridge",
        type=str.lower,
        help="Dictionary to use.",
    )

    return parser.parse_args()


def run_cli(service: EnToEnService, words: list[str], path: str) -> None:
    selections: dict[str, list[Entry]] = {}

    for word in words:
        entries = service.get_word_entries(word)
        if not entries:
            continue

        selected_defs = (
            checkbox(
                f"Select definitions for '{word}'",
                choices=[e.definition for e in entries],
            ).ask()
            or []
        )

        chosen_entries: list[Entry] = []

        for entry in entries:
            if entry.definition not in selected_defs:
                continue

            selected_examples: list[str] = []

            if entry.examples:
                selected_examples = (
                    checkbox(
                        f"Select examples for '{entry.definition}'",
                        choices=entry.examples,
                    ).ask()
                    or []
                )

            chosen_entries.append(
                Entry(
                    spelling=entry.spelling,
                    transcription=entry.transcription,
                    definition=entry.definition,
                    examples=selected_examples,
                )
            )


        if chosen_entries:
            selections[word] = chosen_entries

    notes = service.get_notes_as_strings_from_entries(selections)
    service.save_notes_to_path(notes, path)



def cli_main():
    args = parse_args()

    service = create_service(
        source_lang=args.source,
        target_lang=args.target,
        dictionary_name=args.dictionary,
    )

    run_cli(
        service=service,
        words=args.words,
        path=args.path,
    )
