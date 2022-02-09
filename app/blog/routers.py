from blog import schemas
from fastapi import APIRouter


blog_router = APIRouter()


@blog_router.post("/blogs/{blog_id:int}")
def blogs(blog_id: int, blog: schemas.Blog):
    """Create or update blog by id"""
    print(blog)
    return {"blog_id": blog_id}


@blog_router.get("/blogs/{blog_id:int}")
def blogs(blog_id: int):
    """Get blog by id"""
    return {"blog_id": blog_id}