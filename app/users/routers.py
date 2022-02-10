from users import schemas
from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.orm import Session
from database.database import engine, SessionLocal
from database.models import users as user_model
from users.hashing import Hash
from .custom_token import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm


user_model.User.metadata.create_all(engine)

users_router = APIRouterblog_router = APIRouter(
    prefix="/api/v1",
    tags=['User']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@users_router.post("/users", response_model=schemas.UserShow)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    """Create user"""

    hashed_pwd = Hash.bcrypt(user.password)
    new_user = user_model.User(name=user.name, email=user.email, password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@users_router.get("/users/{user_id}", response_model=schemas.UserShow)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user"""

    get_user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if not get_user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found.")
    return get_user.first()

auth_router = APIRouterblog_router = APIRouter(
    prefix="/api/v1",
    tags=['Auth']
)

@auth_router.post("/auth", response_model=schemas.Token)
def auth_user(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Auth user"""

    get_user = db.query(user_model.User).filter(user_model.User.email == user.username).first()
    if not get_user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Wrong email or email.")
    
    pwd_verify = Hash.verify(user.password, get_user.password)
    if not pwd_verify:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Wrong email or email.")
    
    # generate jwt token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}