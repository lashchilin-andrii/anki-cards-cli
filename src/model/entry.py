from dataclasses import dataclass, field


@dataclass
class Entry:
    spelling: str
    transcription: str
    definition: str
    examples: list[str] = field(default_factory=list)

    def __str__(self, separator: str = "|") -> str:
        return separator.join(
            (
                self.spelling,
                self.transcription,
                self.definition,
                "<br><br>".join(self.examples),
            )
        )
