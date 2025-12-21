from pydantic import BaseModel


class WordEntry(BaseModel):
    spelling: str
    transcription: str
    definition: str
    examples: list[str] = []

    def __str__(self, separator="|") -> str:
        spelling = self.spelling.replace(separator, ";")
        definition = self.definition.replace(separator, ";")
        examples_html = "<br><br>".join(
            example.replace(separator, ";") for example in self.examples
        )
        return f"{spelling}|{self.transcription}|{definition}|{examples_html}"
