import os
import time

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.common import log_config
from app.common.config import GLOBAL_CONFIG
from loguru import logger
from app import (
    router,
)

# 导入日志
log_config.init_logger(level=GLOBAL_CONFIG['logging']['level'])



app = FastAPI()

router.register_default_router(app)
router.register_routers_dynamically(app, api_version='v1')



if __name__ == "__main__":
    import uvicorn

    host = GLOBAL_CONFIG.get('server', {}).get('host', '127.0.0.1')
    port = GLOBAL_CONFIG.get('server', {}).get('port', 8000)
    logger.info("Start server...")
    logger.info(f"接口文档地址：http://{host}:{port}/docs")
    uvicorn.run(app, host=host, port=port)
    logger.info("Server started successfully.")
