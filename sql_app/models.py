from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
import json
from .database import Base
import time
import datetime
  
class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String, index=True)
    mem_expiration = Column(Integer, index=True)
    remaining_punches = Column(Integer, index=True)
    
    visits = relationship("Visit", back_populates="member")


    def __str__(self):
        return str([self.id, self.name, self.address, self.remaining_punches, self.mem_expiration])

    def aslist(self):
        if self.mem_expiration == 0:
            mem_expiration = "No Membership"
        else:
            mem_expiration = datetime.datetime.fromtimestamp(int(self.mem_expiration/1e3)).strftime("%x")

        return [self.id, self.name, self.address, self.remaining_punches, mem_expiration]


class Visit(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"))
    name = Column(String, index=True)
    timein = Column(Integer, index=True)
    timeout = Column(Integer, index=True)

    member = relationship("Member", back_populates="visits")

    

    def __str__(self):
        return str([self.id, self.member_id, self.timein, self.timeout])

    def aslist(self):
        t_in = datetime.datetime.fromtimestamp(int(self.timein) / 1e3)
        if self.timeout:
            t_out = datetime.datetime.fromtimestamp(int(self.timeout) / 1e3)
            #return [self.id, self.member_id, self.name, t_in.strftime("%x %H:%M"), t_out.strftime("%x %H:%M")]
            return [self.id, self.member_id, self.name, t_in.strftime("%H:%M"), t_out.strftime("%H:%M")]
        else:
            return [self.id, self.member_id, self.name, t_in.strftime("%H:%M"), 0]

    def datestr(self):
        return datetime.datetime.fromtimestamp(int(self.timein) / 1e3).strftime("%x")