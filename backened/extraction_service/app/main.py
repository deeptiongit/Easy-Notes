from fastapi import FastAPI
from .routers import extract, erp,client,auth
from database import models, database
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="AI Document Processing Agent")
models.Base.metadata.create_all(bind=database.engine)

app.include_router(extract.router)
app.include_router(erp.router)
app.include_router(client.router)
app.include_router(auth.router)