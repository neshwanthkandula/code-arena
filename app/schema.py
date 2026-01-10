from pydantic import BaseModel
from typing import List

class ProblemOut(BaseModel):
    title : str
    slug : str
    status : str 

    class Config:
        orm_mode = True