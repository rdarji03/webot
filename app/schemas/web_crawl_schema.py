from pydantic import BaseModel


class WebsiteCreate(BaseModel):
    website: str


class WebsiteResponse(BaseModel):
    id: int
    website: str

    class Config:
        orm_mode = True
