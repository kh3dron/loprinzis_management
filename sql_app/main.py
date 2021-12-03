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

@app.get("/dump/")
def read_members(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    mems = crud.get_members(db, skip=skip, limit=limit)
    #this goes line by line
    return mems


@app.get("/", response_class=HTMLResponse)
async def sample(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    members = crud.get_members(db, skip=skip, limit=limit)
    members = [e.aslist() for e in members]
    return templates.TemplateResponse("./welcome.html", {"request": request, "members":members})

@app.get("/register", response_class=HTMLResponse)
async def sample(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return templates.TemplateResponse("./register.html", {"request": request})

@app.get("/today", response_class=HTMLResponse)
async def sample(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    
    visits = [e.aslist() for e in crud.get_visits(db, skip=skip, limit=limit)]

    return templates.TemplateResponse("./today.html", {"request": request, "visits":visits})


@app.post("/create_member/")
def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db)):
    return crud.create_member(db=db, member=member)

@app.post("/create_visit/")
def create_visit(visit: schemas.VisitCreate, db: Session = Depends(get_db)):
    print("Here!")
    db_member = crud.get_member_by_name(db, name=visit.name)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")

    return crud.create_visit(db=db, visit=visit)



@app.get("/members/", response_model=List[schemas.Member])
def read_members(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    members = crud.get_members(db, skip=skip, limit=limit)
    return members


@app.get("/members/{member_id}", response_model=schemas.Member)
def read_member(member_id: int, db: Session = Depends(get_db)):
    db_member = crud.get_member(db, member_id=member_id)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member
