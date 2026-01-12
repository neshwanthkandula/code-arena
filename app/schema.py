from pydantic import BaseModel
from typing import List

class ProblemOut(BaseModel):
    title : str
    slug : str
    status : str 

    class Config:
        orm_mode = True


class SubmitRequest(BaseModel):
    source_code : str 
    problem_slug : str
    language_id : int

    class Config:
        orm_mode = True

class SignupRequest(BaseModel):
    username : str
    email: str
    password : str

    class Config:
        orm_mode = True
class LoginRequest(BaseModel):
    email : str
    password : str

    class Config:
        orm_mode = True

class CreateContestRequest(BaseModel):
    constest_id : str

    class Config:
        orm_mode = True

class ContestSubmitRequest(BaseModel):
    problem_slug : str
    source_code : str
    language_id : int

    class Config:
        orm_mode = True

