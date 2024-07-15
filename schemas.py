from pydantic import BaseModel

class PasteBase(BaseModel):
    title: str
    content: str

class PasteCreate(PasteBase):
    pass

class Paste(PasteBase):
    id: int

    class Config:
        from_attributes = True

