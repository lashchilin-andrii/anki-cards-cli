from dataclasses import dataclass, field

@dataclass
class WordEntry:
    spelling: str
    transcription: str
    definition: str
    examples: list[str] = field(default_factory=list)

    def __str__(self, separator: str = "|") -> str:
        spelling = self.spelling.replace(separator, ";")
        definition = self.definition.replace(separator, ";")
        examples_html = "<br><br>".join(
            example.replace(separator, ";") for example in self.examples
        )
        return f"{spelling}{separator}{self.transcription}{separator}{definition}{separator}{examples_html}"
