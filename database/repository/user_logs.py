from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException,status

def get_all(db: Session):
    blogs = db.query(models.Logs).all()
    return blogs

def create(request: schemas.Logs,db: Session):
    new_log = models.Logs(title=request.title, body=request.body,user_id=1)
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

def destroy(id:int,db: Session):
    log = db.query(models.Logs).filter(models.Logs.id == id)

    if not log.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Log number {id} not found")

    log.delete(synchronize_session=False)
    db.commit()
    return 'done'

def update(id:int,request:schemas.Logs, db:Session):
    log = db.query(models.Logs).filter(models.Logs.id == id)

    if not log.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Log number {id} not found")

    log.update(request)
    db.commit()
    return 'updated'

def show(id:int,db:Session):
    log = db.query(models.Logs).filter(models.Logs.id == id).first()
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Log number {id} not found")
    return log