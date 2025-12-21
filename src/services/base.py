import os
from datetime import date
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def save_notes(path: str, notes: list[str], filename_prefix: str = "words") -> None:
    """
    Save a list of note strings to a .txt file.
    Each note is expected to already be formatted as a string.
    The filename includes the current date.
    """
    today = date.today()

    if not os.path.isdir(path):
        logger.error("Directory does not exist: %s", path)
        return

    final_file = os.path.join(path, f"{filename_prefix}_{today}.txt")

    try:
        with open(final_file, "w", encoding="utf-8") as f:
            for note in notes:
                f.write(note + "\n")
        logger.info("Notes saved successfully: %s", final_file)
    except Exception as e:
        logger.exception("Failed to save notes: %s", e)


def clear_terminal():
    """Clear the terminal screen (cross-platform)."""
    os.system("cls" if os.name == "nt" else "clear")
