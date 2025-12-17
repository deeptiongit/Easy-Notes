from database import database,models
from sqlalchemy.orm import Session
from ..utils import currentuser
from fastapi import APIRouter,Depends,HTTPException
from database import schemas

router = APIRouter(
    tags=["files"],
)

get_db = database.get_feedback_db


@router.delete('/api/files/{file_id}')
def remove_file(file_id:int,db: Session = Depends(get_db), 
                current_user: schemas.client.Client = Depends(currentuser.get_current_client)):
    
    document = db.query(models.DocumentLog).filter(models.DocumentLog.document_id == file_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    db.delete(document)
    db.commit()

