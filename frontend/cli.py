import argparse
from questionary import checkbox

from backend.dictionary import create_service
from backend.dictionary.base.service import BaseService
from backend.dictionary.cambridge.model import Entry


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


def run_cli(service: BaseService, words: list[str], path: str) -> None:
    chosen_entries: list[Entry] = []

    for word in words:
        entries: list = service.get_entry(word)
        if not entries:
            continue

        selected_defs = (
            checkbox(
                f"Select definitions for '{word}'",
                choices=[e.definition for e in entries],
                instruction=str(),
            ).ask()
            or []
        )

        for entry in entries:
            if entry.definition not in selected_defs:
                continue

            selected_examples: list[str] = []

            if entry.examples:
                selected_examples = (
                    checkbox(
                        f"Select examples for '{entry.definition}'",
                        choices=entry.examples,
                        instruction=str(),
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

    service.save_entries_txt(
        entries=[str(entry) for entry in chosen_entries], path=path
    )


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
