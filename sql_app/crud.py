from sqlalchemy.orm import Session

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
    db_visit = models.Visit(member_id=visit.member_id, name=visit.name, timein=visit.timein, timeout=None)
    db.add(db_visit)
    db.commit()
    db.refresh(db_visit)
    return db_visit

def get_visits(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Visit).offset(skip).limit(limit).all()

