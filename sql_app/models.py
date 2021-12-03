from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
import json
from .database import Base
import time
  
class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String, index=True)
    #membership_expiration = Column(Date, index=True)
    remaining_punches = Column(Integer, index=True)
    
    visits = relationship("Visit", back_populates="member")


    def __str__(self):
        return str([self.id, self.name, self.address, self.remaining_punches])

    def aslist(self):
        return [self.id, self.name, self.address, self.remaining_punches]


class Visit(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"))
    name = Column(String, index=True)
    timein = Column(DateTime, index=True)
    timeout = Column(DateTime, index=True)

    member = relationship("Member", back_populates="visits")

    def __str__(self):
        return str([self.id, self.member_id, self.timein, self.timeout])

    def aslist(self):
        return [self.id, self.member_id, self.name, self.timein.strftime("%c"), self.timeout.strftime("%c")]