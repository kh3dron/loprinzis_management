from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
import json
from .database import Base

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, index=True)
    lastname = Column(String, index=True)
    address = Column(String, index=True)
    membership_expiration = Column(Date, index=True)
    remaining_punches = Column(Integer, index=True)


    def __str__(self):
        return str([self.id, self.firstname, self.lastname, self.address, self.membership_expiration, self.remaining_punches])