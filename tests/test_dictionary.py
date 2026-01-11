import pytest
from backend.dictionary.en.en.merriam_webster import MerriamWebsterDictionary
from backend.dictionary.en.en.merriam_webster.model import Word


def test_merriam_webster():
    json = MerriamWebsterDictionary().get_entry("run off")
    word = Word.model_validate_json(json.text)
    print(word.root[0].shortdef)
    for entry in word.root:
        print(entry.shortdef)
