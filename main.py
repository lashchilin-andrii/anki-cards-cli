import warnings

warnings.filterwarnings(
    "ignore", message="pkg_resources is deprecated", category=UserWarning
)

import argparse  # noqa: E402
from src.services import create_service  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description="Create simple Anki-style word cards.")
    parser.add_argument("words", nargs="+", help="List of words separated by spaces.")
    parser.add_argument(
        "-p", "--path", type=str, required=True, help="Path to save the file."
    )
    parser.add_argument(
        "-f",
        "--from",
        dest="source",
        type=str.lower,
        default="en",
        help="Source language code.",
    )
    parser.add_argument(
        "-t",
        "--to",
        dest="target",
        type=str.lower,
        default="en",
        help="Target language code.",
    )
    parser.add_argument(
        "-d",
        "--dictionary",
        type=str.lower,
        default="cambridge",
        help="Dictionary to use.",
    )

    args = parser.parse_args()

    try:
        service = create_service(args.source, args.target, args.dictionary)
    except ValueError as e:
        print(e)
        return

    service.run(args.words, args.path)


if __name__ == "__main__":
    main()
