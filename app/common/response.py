from typing import Union, Mapping

from starlette.background import BackgroundTask
from starlette.responses import JSONResponse
import time

from app.common.status import ErrorCode


class R:

    @staticmethod
    def ok(
            data: Union[dict, list, str] = None,
            msg: str = None,
            code: int = None,
            status: ErrorCode = ErrorCode.SUCCESS,
            http_status_code: int = 200,
            headers: Mapping[str, str] | None = None,
            media_type: str | None = None,
            background: BackgroundTask | None = None,
    ) -> JSONResponse:
        return JSONResponse(
            content={
                "time": time.time(),
                "msg": msg or status.msg,
                "code": code or status.code,
                "data": data,
            },
            status_code=http_status_code,
            headers=headers,
            media_type=media_type,
            background=background,
        )

    @staticmethod
    def fail(
            msg: str = None,
            code: int = None,
            error: Union[str, Exception] = None,
            data: Union[dict, list, str] = None,
            status: ErrorCode = ErrorCode.SUCCESS,
            http_status_code: int = 200,
            headers: Mapping[str, str] | None = None,
            media_type: str | None = None,
            background: BackgroundTask | None = None,
    ) -> JSONResponse:
        return JSONResponse(
            content={
                "time": time.time(),
                "msg": msg or status.msg,
                "code": code or status.code,
                "error": str(error),
                "data": data,
            },
            status_code=http_status_code,
            headers=headers,
            media_type=media_type,
            background=background,
        )
