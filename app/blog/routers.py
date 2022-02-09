from blog import schemas
from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.orm import Session
from database.database import engine, SessionLocal
from database.models import blog as blog_model


# blog_model.Blog.metadata.create_all(engine)

blog_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@blog_router.post("/blogs")
def create_blog(blog: schemas.Blog, db: Session = Depends(get_db)):
    """Create blog"""

    new_blog = blog_model.Blog(title=blog.title, description=blog.description)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@blog_router.get("/blogs/{blog_id:int}")
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    """Get blog by id"""

    blog = db.query(blog_model.Blog).filter(blog_model.Blog.id==blog_id).first()
    if not blog:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {blog_id} not found.")
    return blog


@blog_router.put("/blogs/{blog_id:int}")
def update_blog(blog_id: int, blog: schemas.Blog,  db: Session = Depends(get_db)):
    """Update blog by id"""

    upd_blog = db.query(blog_model.Blog).filter(blog_model.Blog.id==blog_id)
    if not upd_blog.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {blog_id} not found.")
    upd_blog.update(blog.dict())
    db.commit()
    return upd_blog.first()


@blog_router.delete("/blogs/{blog_id:int}")
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    """Delete blog by id"""

    blog = db.query(blog_model.Blog).filter(blog_model.Blog.id==blog_id).first()
    if not blog:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {blog_id} not found.")
    blog.delete(synchronize_session=False)
    db.commit()
    return blog


@blog_router.get("/blogs")
def get_all_blogs(db: Session = Depends(get_db)):
    """Get all blogs"""

    blog = db.query(blog_model.Blog).all()
    return blog