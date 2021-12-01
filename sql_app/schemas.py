from typing import List, Optional
from datetime import date, datetime, time, timedelta
from pydantic import BaseModel


class MemberBase(BaseModel):
    firstname: str
    lastname: str
    address: str
#    membership_expiration: date
    remaining_punches: int


class MemberCreate(MemberBase):
    print("creating")
    pass


class Member(MemberBase):
    id: int

    class Config:
        orm_mode = True