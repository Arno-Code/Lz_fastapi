from sqlalchemy.orm import Session
from app.models import Book, User
from app.schemas import BookCreate, UserCreate

# Book 服务
class BookService:
    @staticmethod
    def create_book(db: Session, book: BookCreate):
        db_book = Book(title=book.title, author=book.author, published_at=book.published_at)
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book

    @staticmethod
    def get_books(db: Session, skip: int = 0, limit: int = 10):
        return db.query(Book).offset(skip).limit(limit).all()

# User 服务
class UserService:
    @staticmethod
    def create_user(db: Session, user: UserCreate):
        db_user = User(username=user.username, password=user.password)  # 请注意实际应用中密码应该加密存储
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
