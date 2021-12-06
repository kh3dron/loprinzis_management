from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
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
    members = crud.get_members(db, skip=skip, limit=limit)
    members = [e.homestr() for e in members]
    return templates.TemplateResponse("./welcome.html", {"request": request, "members":members})

@app.get("/register", response_class=HTMLResponse)
async def sample(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return templates.TemplateResponse("./register.html", {"request": request})

@app.get("/today", response_class=HTMLResponse)
async def sample(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    
    #v = [e.curstr() for e in crud.get_visits(db, skip=skip, limit=limit)]
    curSTR = [e.curstr() for e in crud.get_current_visitors(db, skip=skip, limit=limit)]
    curOBJ = [e.aslist() for e in crud.get_current_visitors(db, skip=skip, limit=limit)]
    hstSTR = [e.histstr() for e in crud.get_past_visitors(db, skip=skip, limit=limit)]

    return templates.TemplateResponse("./today.html", {"request": request, "curSTR":curSTR, "curOBJ":curOBJ, "hstSTR":hstSTR})

@app.post("/create_member/")
def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db)):
    return crud.create_member(db=db, member=member)

@app.post("/create_visit/")
def create_visit(visit: schemas.VisitCreate, db: Session = Depends(get_db)):
    db_member = (crud.get_member_by_name(db, name=visit.name)).aslist()
    if db_member is None:
        raise HTTPException(status_code=200, detail="Member not found")
    visit.name = db_member[1]
    print(visit)
    return crud.create_visit(db=db, visit=visit)

@app.get("/members/", response_model=List[schemas.Member])
def read_members(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    members = crud.get_members(db, skip=skip, limit=limit)
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
def read_member(member_id: int, db: Session = Depends(get_db)):
    db_member = crud.get_member(db, member_id=member_id)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member


@app.post("/checkout/")
def checkout_visit(visit: schemas.Checkout, db: Session = Depends(get_db)):
    print("Checking out!")
    print(visit.member_id)
    return crud.checkout_visit(db=db, member_id=visit.member_id)
