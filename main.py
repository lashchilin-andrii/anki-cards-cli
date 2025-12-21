import warnings

warnings.filterwarnings(
    "ignore", message="pkg_resources is deprecated", category=UserWarning
)

import argparse
from src.services import en_to_en


def main():
    parser = argparse.ArgumentParser(description="Create simple Anki-style word cards.")
    parser.add_argument("words", nargs="+", help="List the words separated by spaces.")
    parser.add_argument(
        "--path", type=str, required=True, help="Path to save the word notes."
    )
    args = parser.parse_args()

    en_to_en.run(args.words, args.path)


if __name__ == "__main__":
    main()
