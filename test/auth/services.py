from app.models import User
from sqlalchemy.orm import Session

class AuthService:
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str):
        user = db.query(User).filter(User.username == username, User.password == password).first()
        if user:
            return {"message": "Authenticated successfully"}
        return {"message": "Invalid credentials"}, 401
