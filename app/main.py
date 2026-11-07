from fastapi import FastAPI
from app.api.router import api_router

app = FastAPI(
    title="AliExpress API",
    description="API de extração e processamento de produtos",
    version="1.0.0"
)

app.include_router(
    api_router,
    prefix="/api/v1"
)


@app.get("/")
def home():
    return {"message": "API online"}