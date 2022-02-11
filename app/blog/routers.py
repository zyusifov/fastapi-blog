from blog import schemas
from users import schemas as users_schemas
from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.orm import Session
from database.database import engine, SessionLocal
from database.models import blog as blog_model
from database.models import users as user_model
from users.oauth2 import get_current_user


blog_model.Blog.metadata.create_all(engine)

blog_router = APIRouter(
    prefix="/api/v1",
    tags=['Blog']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@blog_router.post("/blogs", response_model=schemas.BlogShow)
def create_blog(blog: schemas.Blog, db: Session = Depends(get_db), current_user: users_schemas.User = Depends(get_current_user)):
    """Create blog"""

    user = db.query(user_model.User).filter(user_model.User.email==current_user.email).first()
    new_blog = blog_model.Blog(title=blog.title, description=blog.description, user_id=user.id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@blog_router.get("/blogs/{blog_id}", response_model=schemas.BlogShow)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    """Get blog by id"""

    blog = db.query(blog_model.Blog).filter(blog_model.Blog.id==blog_id).first()
    if not blog:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Blog with id {blog_id} not found.")
    return blog


@blog_router.put("/blogs/{blog_id}", response_model=schemas.BlogShow)
def update_blog(blog_id: int, blog: schemas.Blog,  db: Session = Depends(get_db), current_user: users_schemas.User = Depends(get_current_user)):
    """Update blog by id"""

    user = db.query(user_model.User).filter(user_model.User.email==current_user.email).first()
    upd_blog = db.query(blog_model.Blog).filter(blog_model.Blog.id==blog_id)
    
    if not upd_blog.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Blog with id {blog_id} not found.")
    
    if upd_blog.first().user_id != user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f"You are not the creator of this blog.")

    upd_blog.update(blog.dict())
    db.commit()
    return upd_blog.first()


@blog_router.delete("/blogs/{blog_id}")
def delete_blog(blog_id: int, db: Session = Depends(get_db), current_user: users_schemas.User = Depends(get_current_user)):
    """Delete blog by id"""

    blog = db.query(blog_model.Blog).filter(blog_model.Blog.id==blog_id)
    user = db.query(user_model.User).filter(user_model.User.email==current_user.email).first()

    if not blog.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Blog with id {blog_id} not found.")

    if blog.first().user_id != user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f"You are not the creator of this blog.")

    blog.delete(synchronize_session=False)
    db.commit()
    return HTTPException(status_code = status.HTTP_200_OK, detail=f"Blog deleted.")


@blog_router.get("/blogs")
def get_all_blogs(db: Session = Depends(get_db)):
    """Get all blogs"""

    blog = db.query(blog_model.Blog).all()
    return blog


# current_user: users_schemas.User = Depends(get_current_user)