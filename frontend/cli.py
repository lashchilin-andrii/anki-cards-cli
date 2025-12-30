import argparse
from questionary import checkbox

from src.service import create_service
from src.service.en.en import EnToEnService


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
    selections: dict[str, dict[int, list[int]]] = {}

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

        word_selection: dict[int, list[int]] = {}

        for idx, entry in enumerate(entries):
            if entry.definition not in selected_defs:
                continue

            selected_examples = (
                checkbox(
                    f"Select examples for '{entry.definition}'",
                    choices=entry.examples,
                ).ask()
                or []
            )

            example_indices = [
                entry.examples.index(example) for example in selected_examples
            ]

            word_selection[idx] = example_indices

        selections[word] = word_selection

    notes = service.get_notes_as_strings(words, selections)
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
