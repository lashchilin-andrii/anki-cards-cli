from backend.dictionary.en.en.cambridge import CambridgeDictionary

DICTIONARIES = {
    "cambridge": CambridgeDictionary,
    # "collins": CollinsDictionary
}

from backend.dictionary import DICTIONARIES
from backend.dictionary.en.en.cambridge.service import EnToEnService

SERVICES = {
    ("en", "en"): EnToEnService,
    # ("en", "jp"): EnToJpService,
    # ("jp", "en"): JpToEnService,
}


def create_service(source_lang: str, target_lang: str, dictionary_name: str):
    """
    Factory to create a service instance with the selected dictionary.
    Returns the service instance, or raises ValueError if not found.
    """
    source_lang = source_lang.lower()
    target_lang = target_lang.lower()
    dictionary_name = dictionary_name.lower()

    # ---------- select dictionary ----------
    dictionary_cls = DICTIONARIES.get(dictionary_name)
    if not dictionary_cls:
        raise ValueError(f"Dictionary '{dictionary_name}' not found.")
    dictionary = dictionary_cls()

    # ---------- select service ----------
    service_cls = SERVICES.get((source_lang, target_lang))
    if not service_cls:
        raise ValueError(
            f"No service found for language pair {source_lang}-{target_lang}."
        )
    service = service_cls(dictionary)

    return service
