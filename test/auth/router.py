from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas import AuthRequest
from app.services import AuthService

router = APIRouter()

# 获取数据库会话的依赖函数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(auth_request: AuthRequest, db: Session = Depends(get_db)):
    return AuthService.authenticate_user(db=db, username=auth_request.username, password=auth_request.password)
