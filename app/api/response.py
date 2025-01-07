from typing import Union, Mapping

from starlette.background import BackgroundTask
from starlette.responses import JSONResponse
import time



class R:

    @staticmethod
    def success(
            data: Union[dict, list, str] = None,
            msg: str = None,
            code: int = None,
            status: Status = Status.SUCCESS,
            status_code: int = 200,
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
            status_code=status_code,
            headers=headers,
            media_type=media_type,
            background=background,
        )

    @staticmethod
    def failure(
            msg: str = None,
            code: int = None,
            error: Union[str, Exception] = None,
            data: Union[dict, list, str] = None,
            status: Status = Status.FAILURE,
            status_code: int = 200,
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
            status_code=status_code,
            headers=headers,
            media_type=media_type,
            background=background,
        )

