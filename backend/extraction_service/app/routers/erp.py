from fastapi import APIRouter, Body , Depends
from database import schemas
from ..services.erp_adaptor import push_to_erp
from ..utils import currentuser

router = APIRouter(prefix="/erp", tags=["ERP Integration"])

@router.post("/sync")
async def erp_sync(data: dict = Body(...) ,
                   current_user: schemas.client.Client = Depends(currentuser.get_current_client) ):
    success = push_to_erp(data)
    return {"status": "success" if success else "fail"}