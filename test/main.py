from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.router import router as auth_router
from book.router import router as book_router
from app.database import engine, Base

# 初始化 FastAPI 应用
app = FastAPI()

# 配置 CORS 中间件（如果需要）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)

# 初始化数据库
Base.metadata.create_all(bind=engine)

# 注册路由
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(book_router, prefix="/book", tags=["book"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
