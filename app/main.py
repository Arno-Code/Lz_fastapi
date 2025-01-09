import os

from fastapi import FastAPI

from app.common import log_config
from app.common.config import GLOBAL_CONFIG
from loguru import logger

# 导入日志
log_config.init_logger(level=GLOBAL_CONFIG['logging']['level'])

app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}
#
#
# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}




# @app.post("/uploadfile/")
# async def upload_file(file: UploadFile = File(...)):
#     file_location = os.path.join(UPLOAD_FOLDER, file.filename)
#
#     # 将文件保存到指定路径
#     with open(file_location, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
#
#     return {"filename": file.filename, "location": file_location}
#
#
# @app.get("/downloadfile/{filename}")
# async def download_file(filename: str):
#     file_location = os.path.join(UPLOAD_FOLDER, filename)
#
#     # 检查文件是否存在
#     if not os.path.exists(file_location):
#         raise HTTPException(status_code=404, detail="File not found")
#
#     # 返回文件，用户浏览器会自动下载该文件
#     return FileResponse(file_location, media_type='application/octet-stream', filename=filename)


if __name__ == "__main__":
    import uvicorn
    host = GLOBAL_CONFIG.get('server', {}).get('host', '127.0.0.1')
    port = GLOBAL_CONFIG.get('server', {}).get('port', 8000)
    logger.info("Start server...")
    logger.info(f"接口文档地址：http://{host}:{port}/docs")
    uvicorn.run(app, host=host, port=port)
    logger.info("Server started successfully.")
