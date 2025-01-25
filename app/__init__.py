import uvicorn
from fastapi import FastAPI

from app.common.database import db, lifespan

app = FastAPI(lifespan=lifespan)

from auth.router import router
app.include_router(router)


@app.get("/")
async def root():
    async with db.pool.acquire() as connection:
        query = "SELECT * FROM users"
        row = await connection.fetchrow(query)
        print(row)
        return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8080)
