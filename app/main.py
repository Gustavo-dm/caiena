from fastapi import FastAPI
from app.api.routes import router
from app.api.index import router as index_router
app = FastAPI()

app.include_router(index_router)
app.include_router(router)