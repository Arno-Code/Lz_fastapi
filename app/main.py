import logging
import os
import shutil
from typing import Union

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse

from app.common.config import Config

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# 定义文件保存路径
UPLOAD_FOLDER = "uploads"

# 确保目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)

    # 将文件保存到指定路径
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "location": file_location}


@app.get("/downloadfile/{filename}")
async def download_file(filename: str):
    file_location = os.path.join(UPLOAD_FOLDER, filename)

    # 检查文件是否存在
    if not os.path.exists(file_location):
        raise HTTPException(status_code=404, detail="File not found")

    # 返回文件，用户浏览器会自动下载该文件
    return FileResponse(file_location, media_type='application/octet-stream', filename=filename)


# 配置日志
log_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s [%(filename)s:%(lineno)d - %(funcName)s] - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}


if __name__ == "__main__":
    config = Config()
    # 配置日志级别为DEBUG
    logging.basicConfig(
        level=logging.DEBUG,  # 设置日志级别为 DEBUG，这样所有级别的日志都会被输出
        format='%(asctime)s %(levelname)s [%(filename)s:%(lineno)d - %(funcName)s] - %(message)s',
        handlers=[logging.StreamHandler()]  # 输出到控制台
    )

    logging.info("Starting server...")
    # # 测试输出不同级别的日志信息
    logging.info("This is an info message.")
    logging.debug("This is a debug message.")
    logging.warning("This is a warning message.")
    logging.error("This is an error message.")
    logging.critical("This is a critical message.")
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080, log_config=log_config)
