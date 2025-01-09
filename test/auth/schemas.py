from pydantic import BaseModel

class AuthRequest(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
