import uvicorn
from fastapi import FastAPI
from blog.routers import blog_router

app = FastAPI()


@app.get("/")
def index():
    return {"ok": True}



app.include_router(blog_router)


if __name__ == "__main__":
    uvicorn.run(app='main:app',
                host="0.0.0.0",
                reload=True)