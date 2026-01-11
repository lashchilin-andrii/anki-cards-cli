from pydantic import BaseModel, Field, RootModel


class Meta(BaseModel):
    id: str
    uuid: str
    sort: str
    src: str
    section: str
    stems: list[str]
    offensive: bool


class Sound(BaseModel):
    audio: str
    ref: str
    stat: str


class Pr(BaseModel):
    mw: str
    sound: Sound


class Hwi(BaseModel):
    hw: str
    prs: list[Pr] | None = None


class Sense(BaseModel):
    sn: str
    dt: list[list[str]]


class DtItem(BaseModel):
    t: str


class Sdsense(BaseModel):
    sd: str
    dt: list[list[str | list[DtItem]]]


class SseqItem(BaseModel):
    sense: Sense | None = None
    sn: str | None = None
    dt: list[list[str]] | None = None
    sdsense: Sdsense | None = None


class DtItem1(BaseModel):
    t: str


class DtItem2(BaseModel):
    t: str


class Sdsense1(BaseModel):
    sd: str
    dt: list[list[str]]


class SseqItem1(BaseModel):
    sn: str | None = None
    dt: list[list[str | list[list[list[str | list[DtItem1]]] | DtItem2]]]
    sls: list[str] | None = None
    sdsense: Sdsense1 | None = None


class DefItem(BaseModel):
    sseq: list[list[list[str | list[list[str | SseqItem]] | SseqItem1]]]
    vd: str | None = None


class Sound1(BaseModel):
    audio: str
    ref: str
    stat: str


class Pr1(BaseModel):
    mw: str
    sound: Sound1


class In(BaseModel):
    if_: str = Field(..., alias="if")
    ifc: str | None = None
    prs: list[Pr1] | None = None


class Sound2(BaseModel):
    audio: str
    ref: str
    stat: str


class Pr2(BaseModel):
    mw: str
    sound: Sound2


class Uro(BaseModel):
    ure: str
    prs: list[Pr2] | None = None
    fl: str


class Entry(BaseModel):
    meta: Meta
    hom: int | None = None
    hwi: Hwi
    fl: str
    def_: list[DefItem] = Field(..., alias="def")
    et: list[list[str]] | None = None
    date: str | None = None
    shortdef: list[str]
    ins: list[In] | None = None
    uros: list[Uro] | None = None
    dxnls: list[str] | None = None


class Word(RootModel[list[Entry]]):
    pass
