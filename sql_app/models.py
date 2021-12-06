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
    #membership_expiration = Column(Date, index=True)
    remaining_punches = Column(Integer, index=True)
    
    visits = relationship("Visit", back_populates="member")


    def __str__(self):
        return str([self.id, self.name, self.address, self.remaining_punches])

    def aslist(self):
        return [self.id, self.name, self.address, self.remaining_punches]

    def homestr(self):
        return self.name + " | Address: " + self.address + " | Remaining punches: " + str(self.remaining_punches)


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
        else:
            t_out = 0
        #TODO: this memberID isn't populating
        return [self.id, self.member_id, self.name, str(t_in), str(t_out)]

    #current string form
    def curstr(self):
        t_in = datetime.datetime.fromtimestamp(int(self.timein) / 1e3).strftime("%X")

        return  self.name + " came in at " + str(t_in)

    #historic string form
    def histstr(self):
        t_in = datetime.datetime.fromtimestamp(int(self.timein) / 1e3).strftime("%X")
        if self.timeout:
            t_out = datetime.datetime.fromtimestamp(int(self.timeout) / 1e3).strftime("%X")
            return self.name + " came at " + str(t_in) + " and left at " + str(t_out)
        return