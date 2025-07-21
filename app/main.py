from fastapi import FastAPI
from app.routes.webscrap import router as webscrap_router

app = FastAPI()

app.include_router(webscrap_router, prefix='/api')


@app.get('/')
def root():
    return {"message": "API Started"}
