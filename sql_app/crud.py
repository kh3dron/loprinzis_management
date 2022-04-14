from sqlalchemy.orm import Session
import time
from datetime import datetime

from . import models, schemas


def get_member(db: Session, member_id: int):
    return db.query(models.Member).filter(models.Member.id == member_id).first()


def get_member_by_name(db: Session, name: str):
    if name is not None:
        return db.query(models.Member).filter(models.Member.name == name).first()
    else:
        return []

def get_members(db: Session, skip: int = 0, limit: int = 10000):
    return db.query(models.Member).offset(skip).all()

def update_member_punches(db: Session, member_id: int, punches: int):
    obj = db.query(models.Member).filter(models.Member.id == member_id).first()
    obj.remaining_punches = punches
    return db.commit()

def update_member_name(db: Session, member_id: int, name: str):
    obj = db.query(models.Member).filter(models.Member.id == member_id).first()
    obj.name = name
    return db.commit()


def update_member_address(db: Session, member_id: int, address: str):
    obj = db.query(models.Member).filter(models.Member.id == member_id).first()
    obj.address = address
    return db.commit()

def update_member_membership(db: Session, member_id: int, membership):
    obj = db.query(models.Member).filter(models.Member.id == member_id).first()
    obj.mem_expiration = membership
    return db.commit()



def create_member(db: Session, member: schemas.MemberCreate):
    db_member = models.Member(name=member.name, address=member.address,
                            remaining_punches=member.remaining_punches, mem_expiration=member.mem_expiration)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

def create_visit(db: Session, visit: schemas.VisitCreate):
    #get member and decrement from punches
    memb = (db.query(models.Member).filter(models.Member.name == visit.name).first())
    memb.remaining_punches = memb.remaining_punches -1
    db.commit()
    pulled_member_id=memb.id
    already_here = db.query(models.Visit).filter(models.Visit.member_id == pulled_member_id).filter(models.Visit.timeout == 0).all()
    if already_here:
        return "Error: Already checked in!"
    db_visit = models.Visit(member_id=pulled_member_id, name=visit.name, timein=visit.timein, timeout=0)
    db.add(db_visit)
    db.commit()
    db.refresh(db_visit)
    return db_visit

def get_visits(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.Visit).offset(skip).limit(limit).all()

def get_visit(db: Session, member_id: int):
    return db.query(models.Visit).filter(models.Visit.member_id == member_id).first()

def checkout_visit(db: Session, member_id: int, timeout: int):
    mem = db.query(models.Visit).filter(models.Visit.member_id == member_id, models.Visit.timeout == 0).first()
    if not mem:
        return "Visitor not checked in!"
    mem.timeout = timeout
    return db.commit()

def get_current_visitors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Visit).filter(models.Visit.timeout == 0).all()

def get_past_visitors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Visit).filter(models.Visit.timeout != 0).all()

def get_visits_of_date(date, db: Session, skip: int = 0):
    dt = datetime.strptime(date, "%m/%d/%y")
    day_min = int((time.mktime(dt.timetuple()))*1000)
    day_max = day_min + 86399000
    return db.query(models.Visit).filter(models.Visit.timein >= day_min).filter(models.Visit.timein <= day_max).all()