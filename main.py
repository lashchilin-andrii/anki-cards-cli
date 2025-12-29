import warnings

warnings.filterwarnings(
    "ignore", message="pkg_resources is deprecated", category=UserWarning
)

import argparse  # noqa: E402
from src.services.en.en.en_to_en import EnToEnService  # noqa: E402
from src.dictionaries.cambridge import CambridgeDictionary  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description="Create simple Anki-style word cards.")
    parser.add_argument("words", nargs="+", help="List the words separated by spaces.")
    parser.add_argument(
        "--path", type=str, required=True, help="Path to save the file."
    )
    args = parser.parse_args()

    EnToEnService(CambridgeDictionary()).run(args.words, args.path)


if __name__ == "__main__":
    main()
