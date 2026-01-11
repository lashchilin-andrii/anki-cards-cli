import requests

from backend.dictionary.base_dictionary import BaseDictionary

CAMBRIDGE_URL = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key=e0421ef0-ba6d-423d-b246-4946c719d94a"


class MerriamWebsterDictionary(BaseDictionary):
    name = "Merriam Webster"

    def get_entry(self, word: str) -> list:
        entry_json = requests.get(CAMBRIDGE_URL.format(word=word))
        return entry_json
