from dataclasses import dataclass, field
from typing import Literal


@dataclass
class Entry:
    spelling: str = ""
    transcription: str = ""
    definition: str = ""
    examples: list[str] = field(default_factory=list)
    _separator: Literal["|", ",", ";"] = "|"
    _examples_separator_html: str = "<br><br>"

    def __str__(self) -> str:
        return self._separator.join(
            (
                self.spelling,
                self.transcription,
                self.definition,
                self._examples_separator_html.join(self.examples),
            )
        )
