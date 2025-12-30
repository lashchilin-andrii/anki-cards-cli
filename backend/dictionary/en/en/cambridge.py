import requests
from bs4 import BeautifulSoup as BS
import pronouncing

from backend.model.entry import Entry
from backend.dictionary.base import BaseDictionary

CAMBRIDGE_URL = "https://dictionary.cambridge.org/dictionary/english/{word}"

# =======================
# PRONUNCIATION UTILITIES
# =======================

ARPA_TO_IPA = {
    "AA": "ɑ",
    "AE": "æ",
    "AH": "ʌ",
    "AO": "ɔ",
    "AW": "aʊ",
    "AY": "aɪ",
    "B": "b",
    "CH": "tʃ",
    "D": "d",
    "DH": "ð",
    "EH": "ɛ",
    "ER": "ɝ",
    "EY": "eɪ",
    "F": "f",
    "G": "ɡ",
    "HH": "h",
    "IH": "ɪ",
    "IY": "i",
    "JH": "dʒ",
    "K": "k",
    "L": "l",
    "M": "m",
    "N": "n",
    "NG": "ŋ",
    "OW": "oʊ",
    "OY": "ɔɪ",
    "P": "p",
    "R": "ɹ",
    "S": "s",
    "SH": "ʃ",
    "T": "t",
    "TH": "θ",
    "UH": "ʊ",
    "UW": "u",
    "V": "v",
    "W": "w",
    "Y": "j",
    "Z": "z",
    "ZH": "ʒ",
}


def convert_arpa_to_ipa(arpa: str) -> str:
    result = []
    for symbol in arpa.split():
        symbol = "".join(c for c in symbol if not c.isdigit())
        ipa = ARPA_TO_IPA.get(symbol)
        if ipa:
            result.append(ipa)
    return "".join(result)


def get_pronouncing(word: str) -> str:
    ipa_words = []
    for w in word.split():
        phones = pronouncing.phones_for_word(w.lower())
        if phones:
            ipa_words.append(convert_arpa_to_ipa(phones[0]))
    return " ".join(ipa_words)


def get_first_us_transcription(soup: BS) -> str | None:
    us_block = soup.find("span", class_="us dpron-i")
    if not us_block:
        return None
    ipa_span = us_block.find("span", class_="ipa")
    return ipa_span.get_text(strip=True) if ipa_span else None


# ==================
# PARSING UTILITIES
# ==================


def parse_definitions(soup: BS) -> list:
    return soup.find_all("div", class_="ddef_h")


def extract_definition_text(block) -> str | None:
    div = block.find("div", class_="def ddef_d db")
    if not div:
        return None
    return " ".join(div.get_text(separator=" ").split()).replace(":", "").strip()


def extract_examples(block) -> list[str]:
    examples = []
    def_body = block.find_next_sibling("div", class_="def-body ddef_b")
    if not def_body:
        return examples

    for ex in def_body.find_all("div", class_="examp dexamp"):
        text = " ".join(ex.get_text(separator=" ").split()).strip()
        if text:
            examples.append(text)
    return examples


def build_entries(
    word: str,
    blocks: list,
    transcription: str | None,
) -> list[Entry]:
    entries: list[Entry] = []
    seen_defs: set[str] = set()

    for block in blocks:
        definition = extract_definition_text(block)
        if not definition or definition in seen_defs:
            continue

        seen_defs.add(definition)
        examples = extract_examples(block)

        entries.append(
            Entry(
                spelling=word,
                transcription=transcription or "",
                definition=definition,
                examples=examples,
            )
        )

    return entries


# ==================
# DICTIONARY CLASS
# ==================


class CambridgeDictionary(BaseDictionary):
    name = "Cambridge"

    def _fetch_html(self, word: str) -> str | None:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/91.0.4472.124 Safari/537.36"
            )
        }
        try:
            response = requests.get(
                CAMBRIDGE_URL.format(word=word),
                headers=headers,
                timeout=10,
            )
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"[{self.name}] Cannot access '{word}': {e}")
            return None

    def get_entry(self, word: str) -> list[Entry]:
        html = self._fetch_html(word)
        if not html:
            return []

        soup = BS(html, "lxml")
        blocks = parse_definitions(soup)
        if not blocks:
            print(f"[{self.name}] Entry '{word}' not found.")
            return []

        transcription = get_pronouncing(word) or get_first_us_transcription(soup)

        return build_entries(word, blocks, transcription)
