from sqlalchemy.orm import Session
import time

from . import models, schemas


def get_member(db: Session, member_id: int):
    return db.query(models.Member).filter(models.Member.id == member_id).first()


def get_member_by_name(db: Session, name: str):
    return db.query(models.Member).filter(models.Member.name == name).first()


def get_members(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Member).offset(skip).limit(limit).all()


def create_member(db: Session, member: schemas.MemberCreate):
    db_member = models.Member(name=member.name, address=member.address,
                            remaining_punches=member.remaining_punches)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

def create_visit(db: Session, visit: schemas.VisitCreate):

    pulled_member_id = (db.query(models.Member).filter(models.Member.name == visit.name).first()).id
    already_here = db.query(models.Visit).filter(models.Visit.member_id == visit.member_id, models.Visit.timeout == 0).first()
    if already_here is not None:
        return "Error: Already checked in!"
    db_visit = models.Visit(member_id=pulled_member_id, name=visit.name, timein=visit.timein, timeout=0)
    db.add(db_visit)
    db.commit()
    db.refresh(db_visit)
    return db_visit

def get_visits(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Visit).offset(skip).limit(limit).all()

def get_visit(db: Session, member_id: int):
    return db.query(models.Visit).filter(models.Visit.member_id == member_id).first()

def checkout_visit(db: Session, member_id: int):
    mem = db.query(models.Visit).filter(models.Visit.member_id == member_id, models.Visit.timeout == 0).first()
    if not mem:
        return "Visitor not checked in!"
    mem.timeout = int(time.time())
    return db.commit()

def get_current_visitors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Visit).filter(models.Visit.timeout == 0).all()

def get_past_visitors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Visit).filter(models.Visit.timeout != 0).all()
