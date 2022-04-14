from typing import List, Optional
from datetime import date, datetime, time, timedelta
from pydantic import BaseModel


class MemberBase(BaseModel):
    name: str
    address: str
    remaining_punches: int
    mem_expiration: int


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
    timeout: int

class PunchUpdate(BaseModel):
    member_id: int
    punches: int

class NameUpdate(BaseModel):
    member_id: int
    name: str

class AddressUpdate(BaseModel):
    member_id: int
    address: str

class MembershipUpdate(BaseModel):
    member_id: int
    date: int

class DateVisits(BaseModel):
    date: str

class MemberLookup(BaseModel):
    name: str