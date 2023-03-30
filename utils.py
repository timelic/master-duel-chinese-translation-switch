import logging
import os
import sys
from threading import Timer
from typing import Callable, TypeVar, List as list
from typing_extensions import ParamSpec


def getFilesList(path: str) -> list[str]:
    res: list[str] = []
    for _, _, files in os.walk(path):
        res = files  # 文件名称，返回list类型
    return res


T = TypeVar("T")


def flatten(l: list[list[T]]) -> list[T]:
    return [item for sublist in l for item in sublist]


def make_dir(path: str) -> None:
    folder: bool = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径


def get_resource_path(relative_path: str) -> str:
    # 是否Bundle Resource
    if getattr(sys, "frozen", False):
        base_path: str = sys._MEIPASS  # type: ignore
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def q2b_string(ustring):
    """字符串 全角转半角"""

    def q2b_char(uchar: str) -> str:
        """单个字符 全角转半角"""
        inside_code = ord(uchar)
        if inside_code == 0x3000:
            inside_code = 0x0020
        else:
            inside_code -= 0xFEE0
        if inside_code < 0x0020 or inside_code > 0x7E:  # 转完之后不是半角字符返回原来的字符
            return uchar
        return chr(inside_code)

    return "".join([q2b_char(uchar) for uchar in ustring])


P = ParamSpec("P")


def throttle(wait_sec: int) -> Callable[[Callable[P, None]], Callable[P, None]]:
    running = False

    def decorator(fn: Callable[P, None]) -> Callable[P, None]:
        def debounced(*args: P.args, **kwargs: P.kwargs) -> None:
            nonlocal running
            if running:
                return
            running = True
            fn(*args, **kwargs)

            def stop():
                nonlocal running
                running = False

            t = Timer(wait_sec, stop)
            t.start()

        return debounced

    return decorator


def get_logger() -> logging.Logger:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s | %(pathname)s"
    )

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.WARNING)
    stdout_handler.setFormatter(formatter)

    file_handler = logging.FileHandler("No_86_logs.txt")
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)

    return logger
