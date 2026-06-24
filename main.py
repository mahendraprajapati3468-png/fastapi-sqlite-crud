from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base,Session
from sqlalchemy import Column,Integer,String
from fastapi import FastAPI,Depends,HTTPException


database = "sqlite:///./test.db"

app=FastAPI()


engine = create_engine(
    database

)


sessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class mpp(Base):
    __tablename__ = "Student"
    id= Column(Integer,primary_key=True, index=True)
    name=Column(String)
    email=Column(String)


Base.metadata.create_all(bind=engine)

def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/create")
def create_user(name:str,email:str,db:Session=Depends(get_db)):
    cr=mpp(name=name,email=email)
    db.add(cr)
    db.commit()
    db.refresh(cr)
    return{
        "Massege":"Data Added",
        "Data":cr
    }



@app.get("/Read")
def Read(db:Session = Depends(get_db)):
    r=db.query(mpp).all()

    return{
        "Total":len(r),
        "data":r
    }

@app.get("/R_id/{Read_id}")
def Re(Read_id:int,db: Session = Depends(get_db)):
    q=db.query(mpp).filter(mpp.id==Read_id).first()

    if not q:
        raise HTTPException(status_code=404,detail="Data Not Found")
    return q


@app.put("/update/{user_id}")
def up(user_id: int,name: str,email: str,db: Session = Depends(get_db)):
    UP = db.query(mpp).filter(mpp.id == user_id).first()

    if not UP:
        raise HTTPException(
            status_code=404,
            detail="Data Not Found"
        )

    UP.name = name
    UP.email = email

    db.commit()
    db.refresh(UP)

    return {
        "Message": "Data Updated",
        "data": UP
    }



@app.delete("/Delete/{delet_id}")
def dele(del_id:int,db:Session=Depends(get_db)):
    remove= db.query(mpp).filter(mpp.id == del_id).first()


    if not remove:
        raise HTTPException(
            status_code=404,
            detail="Data Not Found"
        )
    db.delete(remove)
    db.commit()

    return{
        "Massege":"Data Deleted"
    }