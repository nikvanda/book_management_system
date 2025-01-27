import uvicorn
from fastapi import FastAPI

from app.common import lifespan
from app.auth.router import router as auth_router
from app.books.router import router as books_router

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, tags=["auth"])
app.include_router(books_router, tags=["books"])

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080)
