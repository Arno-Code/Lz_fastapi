import inspect
import logging
import sys
from typing import Union

from loguru import logger

level_ = "DEBUG"
folder_ = "../log/"
prefix_ = "lz-"
rotation_ = "10 MB"
retention_ = "30 days"
encoding_ = "utf-8"
backtrace_ = True
diagnose_ = True

# 格式里面添加了process和thread记录，方便查看多进程和线程程序
format_ = '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> ' \
          '| <magenta>{process}({process.name})</magenta>:<yellow>{thread}({thread.name})</yellow> ' \
          '| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<yellow>{line}</yellow> - <level>{message}</level>'


# 拦截logging发往 Loguru 接收器的标准消息
class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def init_logger(level: str = level_, format: str = format_, folder: str = folder_
                 , prefix: str = prefix_, rotation: str = rotation_, retention: str = retention_
                 , encoding: str = encoding_, backtrace: bool = backtrace_, diagnose: bool = diagnose_) -> None:
    """
    配置并设置一个 Loguru 日志系统。

    参数：
    --------
    folder : str
        日志文件存储的目录。默认为 `folder_` 的值。
    prefix : str
        日志文件名的前缀。默认为 `prefix_` 的值。
    rotation : str
        日志文件的最大大小或时间周期，达到指定限制时会自动旋转日志文件。示例：`"10 MB"`、`"1 day"`。默认为 `rotation_` 的值。
    retention : str
        保留旧日志文件的时间长度。示例：`"30 days"`、`"1 week"`。默认为 `retention_` 的值。
    encoding : str
        日志文件使用的字符编码。默认为 `encoding_` 的值。
    backtrace : bool
        是否在日志中包含异常回溯信息。默认为 `backtrace_` 的值。
    diagnose : bool
        是否在日志中包含详细的诊断信息（用于调试）。默认为 `diagnose_` 的值。

    返回：
    --------
    None

    示例：
    --------
    >>> logger = setup_logger()
    >>> logger.info("日志系统已初始化！")
    @rtype: object
    """
    # 将loging拦截到loguru
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    logger.remove()  # 移除默认的处理器
    # 这里面采用了层次式的日志记录方式，就是低级日志文件会记录比他高的所有级别日志，这样可以做到低等级日志最丰富，高级别日志更少更关键
    # info
    logger.add(folder + prefix + "info.log", level="INFO", backtrace=backtrace, diagnose=diagnose,
               format=format, colorize=False,
               rotation=rotation, retention=retention, encoding=encoding,
               filter=lambda record: record["level"].no >= logger.level("INFO").no)

    # error
    logger.add(folder + prefix + "error.log", level="ERROR", backtrace=backtrace, diagnose=diagnose,
               format=format, colorize=False,
               rotation=rotation, retention=retention, encoding=encoding,
               filter=lambda record: record["level"].no >= logger.level("ERROR").no)

    # 控制台输出
    logger.add(sys.stderr, level=level, backtrace=backtrace, diagnose=diagnose,
               format=format, colorize=True)
