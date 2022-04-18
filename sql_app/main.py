from distutils.log import warn
from sqlite3 import Timestamp
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
from datetime import date
import uvicorn

from . import loggerconfig
log = loggerconfig.structlog.get_logger("AAAAAAAAAAAA")
log.critical("loaded", meta={"sample":"text", "nest":{"key":"value"}})

models.Base.metadata.create_all(bind=engine)
app = FastAPI() #overwrite logger here
templates = Jinja2Templates(directory="templates")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def sample(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    log.critical("loadaed main page", var1="fish", meta={"a meta":"dictionary"})  
    members = crud.get_members(db, skip=skip)
    members = [e.aslist() for e in members]
    return templates.TemplateResponse("./welcome.html", {"request": request, "members":members})

@app.get("/register", response_class=HTMLResponse)
async def sample(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    memb_OBJ   = json.dumps([e.aslist()[1] for e in crud.get_members(db, skip=skip)])
    memnames   = json.dumps([e.aslist()[1] for e in crud.get_members(db, skip=skip)])
    sm = []

    return templates.TemplateResponse("./register.html", {"request": request, "mems":memnames, "selected_mem":sm})

@app.get("/register/{member_id}", response_class=HTMLResponse)
async def sample(member_id: int, request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    memb_OBJ   = json.dumps([e.aslist()[1] for e in crud.get_members(db, skip=skip)])
    memnames   = json.dumps([e.aslist()[1] for e in crud.get_members(db, skip=skip)])
    sm = crud.get_member(db, member_id).aslist()
    return templates.TemplateResponse("./register.html", {"request": request, "mems":memnames, "selected_mem":sm})


@app.get("/today", response_class=HTMLResponse)
async def sample(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    
    mems   = json.dumps([e.aslist()[1] for e in crud.get_members(db, skip=skip)])
    curOBJ = [e.aslist() for e in crud.get_current_visitors(db, skip=skip, limit=limit)]
    today = date.today().strftime("%m/%d/%y")
    hstOBJ = [e.aslist() for e in crud.get_visits_of_date(today, db, skip=skip)]

    return templates.TemplateResponse("./today.html", {"request": request, "curOBJ":curOBJ, "hstOBJ":hstOBJ, "mems":mems})

@app.get("/queries", response_class=HTMLResponse)
async def sample(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    hst = [e.aslist() for e in crud.get_visits(db, skip=skip)]
    hst.reverse()
    return templates.TemplateResponse("./queries.html", {"request": request, "hst":hst})


@app.post("/create_member/")
def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db)):
    return crud.create_member(db=db, member=member)

@app.post("/create_visit/")
def create_visit(visit: schemas.VisitCreate, db: Session = Depends(get_db)):
    db_member = (crud.get_member_by_name(db, name=visit.name)).aslist()
    if db_member is None:
        raise HTTPException(status_code=200, detail="Member not found")
    visit.name = db_member[1]
    return crud.create_visit(db=db, visit=visit)

@app.get("/members/", response_model=List[schemas.Member])
def read_members(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    members = crud.get_members(db, skip=skip)
    return members

@app.get("/visits/")
def read_visits(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    visits = crud.get_visits(db, skip=skip, limit=limit)
    return visits

@app.get("/visit/{member_id}")
def get_visit(member_id: int, db: Session = Depends(get_db)):
    visit = crud.get_visit(db, member_id = member_id)
    if visit is None:
        raise HTTPException(status_code=404, detail="Member not visiting")
    return visit

@app.get("/members/{member_id}", response_model=schemas.Member)
def get_member_by_id(member_id: int, db: Session = Depends(get_db)):
    db_member = crud.get_member(db, member_id=member_id)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member


@app.post("/checkout/")
def checkout_visit(visit: schemas.Checkout, db: Session = Depends(get_db)):
    return crud.checkout_visit(db=db, member_id=visit.member_id, timeout=visit.timeout)

@app.post("/update_member_punches/")
def update_member_punches(update: schemas.PunchUpdate, db: Session = Depends(get_db)):
    return crud.update_member_punches(db=db, member_id=update.member_id, punches=update.punches)

@app.post("/update_member_name/")
def update_member_name(update: schemas.NameUpdate, db: Session = Depends(get_db)):
    return crud.update_member_name(db=db, member_id=update.member_id, name=update.name)

@app.post("/update_member_address/")
def update_member_address(update: schemas.AddressUpdate, db: Session = Depends(get_db)):
    return crud.update_member_address(db=db, member_id=update.member_id, address=update.address)

@app.post("/update_member_membership/")
def update_member_membership(update: schemas.MembershipUpdate, db: Session = Depends(get_db)):
    return crud.update_member_membership(db=db, member_id=update.member_id, membership=update.date)

@app.post("/date_visits/")
def date_visits(req: schemas.DateVisits, db: Session = Depends(get_db)):
    return crud.get_visits_of_date(db=db, date=req.date)

@app.post("/member_lookup/")
def get_member_by_name(req: schemas.MemberLookup, db: Session = Depends(get_db)):
    return crud.get_member_by_name(db=db, name=req.name)
