from typing import List, Optional
from datetime import date, datetime, time, timedelta
from pydantic import BaseModel


class MemberBase(BaseModel):
    name: str
    address: str
#    membership_expiration: date
    remaining_punches: int


class MemberCreate(MemberBase):
    pass


class Member(MemberBase):
    id: int

    class Config:
        orm_mode = True


class VisitBase(BaseModel):
    member_id: int
    name: str
    timein: int
    timeout: int

class VisitCreate(VisitBase):
    pass

class Checkout(BaseModel):
    member_id: int