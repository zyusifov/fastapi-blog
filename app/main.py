import uvicorn
from fastapi import FastAPI
from blog.routers import blog_router
from users.routers import users_router, auth_router


app = FastAPI()


app.include_router(blog_router)
app.include_router(users_router)
app.include_router(auth_router)


if __name__ == "__main__":
    uvicorn.run(app='main:app', host="0.0.0.0", reload=True)
