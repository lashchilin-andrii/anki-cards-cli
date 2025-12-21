import requests
from bs4 import BeautifulSoup as BS
import pronouncing
from src.models.word_entry import WordEntry

CAMBRIDGE_URL = "https://dictionary.cambridge.org/dictionary/english/{word}"

ARPA_TO_IPA = {
    "AA": "ɑ", "AE": "æ", "AH": "ʌ", "AO": "ɔ", "AW": "aʊ", "AY": "aɪ",
    "B": "b", "CH": "tʃ", "D": "d", "DH": "ð", "EH": "ɛ", "ER": "ɝ",
    "EY": "eɪ", "F": "f", "G": "ɡ", "HH": "h", "IH": "ɪ", "IY": "i",
    "JH": "dʒ", "K": "k", "L": "l", "M": "m", "N": "n", "NG": "ŋ",
    "OW": "oʊ", "OY": "ɔɪ", "P": "p", "R": "ɹ", "S": "s", "SH": "ʃ",
    "T": "t", "TH": "θ", "UH": "ʊ", "UW": "u", "V": "v", "W": "w",
    "Y": "j", "Z": "z", "ZH": "ʒ",
}


def _fetch_html(word: str) -> str | None:
    """Fetch the HTML content of a Cambridge Dictionary page."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        )
    }
    try:
        response = requests.get(CAMBRIDGE_URL.format(word=word), headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Cannot access dictionary for '{word}': {e}")
        return None


def _parse_definitions(soup: BS) -> list:
    """Return all definition blocks from a Cambridge dictionary page."""
    return soup.find_all("div", class_="ddef_h")


def _extract_definition_text(block) -> str | None:
    """Extract text from a definition block."""
    div = block.find("div", class_="def ddef_d db")
    if not div:
        return None
    return " ".join(div.get_text(separator=" ").split()).replace(":", "").strip()


def _extract_examples(block) -> list[str]:
    """Extract example sentences from a definition block."""
    examples = []
    def_body = block.find_next_sibling("div", class_="def-body ddef_b")
    if not def_body:
        return examples
    for ex in def_body.find_all("div", class_="examp dexamp"):
        text = " ".join(ex.get_text(separator=" ").split()).strip()
        if text:
            examples.append(text)
    return examples


def _get_first_us_transcription(soup: BS) -> str | None:
    """Get the first US IPA transcription from the page."""
    us_block = soup.find("span", class_="us dpron-i")
    if not us_block:
        return None
    ipa_span = us_block.find("span", class_="ipa")
    return ipa_span.get_text(strip=True) if ipa_span else None


def _convert_arpa_to_ipa(arpa: str) -> str:
    """Convert ARPAbet symbols to IPA."""
    result = []
    for symbol in arpa.split():
        symbol = "".join(c for c in symbol if not c.isdigit())
        if symbol in ARPA_TO_IPA:
            result.append(ARPA_TO_IPA[symbol])
    return "".join(result)


def get_first_pronouncing(word: str) -> str:
    """Get IPA transcription using the pronouncing library."""
    ipa_words = []
    for w in word.split():
        phones_list = pronouncing.phones_for_word(w.lower())
        if not phones_list:
            continue
        ipa_words.append(_convert_arpa_to_ipa(phones_list[0]))
    return " ".join(ipa_words)


def _build_entries(word: str, blocks: list, transcription: str | None) -> list[WordEntry]:
    """Build WordEntry objects from definition blocks, avoiding duplicates."""
    entries, seen_defs = [], set()
    for block in blocks:
        definition = _extract_definition_text(block)
        if not definition or definition in seen_defs:
            continue
        seen_defs.add(definition)
        examples = _extract_examples(block)
        entries.append(WordEntry(spelling=word, transcription=transcription or "", definition=definition, examples=examples))
    return entries


def get_word_entry(word: str) -> list[WordEntry]:
    """Fetch WordEntry objects (definitions, examples, transcription) from Cambridge Dictionary."""
    html = _fetch_html(word)
    if not html:
        return []

    soup = BS(html, "lxml")
    definition_blocks = _parse_definitions(soup)
    if not definition_blocks:
        print(f"Entry '{word}' not found.")
        return []

    try:
        transcription = get_first_pronouncing(word)
    except IndexError:
        transcription = _get_first_us_transcription(soup)

    return _build_entries(word, definition_blocks, transcription)
