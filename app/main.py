from fastapi import FastAPI
from app.api.v1.auth import router as auth_router
from app.api.v1.categories import router as categories_router
from app.api.v1.articles import router as articles_router
from app.api.v1.images import router as images_router

app = FastAPI(title="Marketplace Blog API")

app.include_router(auth_router)
app.include_router(categories_router)
app.include_router(articles_router)
app.include_router(images_router)

@app.get("/")
async def root():
    return {"message": "йоу!"}
