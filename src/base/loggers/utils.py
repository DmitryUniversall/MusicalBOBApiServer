import inspect
import logging
import time
from datetime import datetime
from functools import wraps
from typing import Any, Callable


def format_time(ts: float) -> str:
    return datetime.fromtimestamp(ts).astimezone().strftime("%H:%M:%S.%f")[:-3]


def log_function(
        logger_name: str | None = None,
        log_result: bool = False,
        log_level: int = logging.DEBUG,
        log_time: bool = False
):
    """
    Decorator to log a function

    :param logger_name: `str | None`
        The custom name of the logger.
        If None, it should be set outside the decorator for class usage.

    :param log_result: `bool`
        Whether to log the result of the async function.
        Default False.

    :param log_level: `int`
        Logging level.
        Default logging.DEBUG.

    :param log_time: `bool`
        Whether to log start and finish time.
        Default False.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        logger = logging.getLogger(logger_name if logger_name is not None else f"calls.{func.__module__}.{func.__qualname__}")  # type: ignore

        if inspect.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs) -> Any:
                start_timestamp = time.time()

                if log_time:
                    logger.log(log_level, f"Called {func.__qualname__} at {format_time(start_timestamp)}")

                result = await func(*args, **kwargs)

                if log_result:
                    logger.log(log_level, f"Got result from {func.__qualname__}: {result}")

                if log_time:
                    logger.log(log_level, f"Finished {func.__qualname__} at {format_time(time.time())} (in {time.time() - start_timestamp:.4f}s)")

                return result

            return async_wrapper
        else:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                start_timestamp = time.time()

                if log_time:
                    logger.log(log_level, f"Called {func.__qualname__} at {format_time(start_timestamp)}")

                result = func(*args, **kwargs)

                if log_result:
                    logger.log(log_level, f"Got result from {func.__qualname__}: {result}")

                if log_time:
                    logger.log(log_level, f"Finished {func.__qualname__} at {format_time(time.time())} (in {time.time() - start_timestamp:.4f}s)")

                return result

            return wrapper

    return decorator


def log_async_methods(
        logger_name: str | None = None,
        log_result: bool = False,
        log_level: int = logging.DEBUG,
        log_time: bool = False
):
    """
    A decorator function for logging all async methods of class.

    :param logger_name: `str | None`
        The custom name of the logger, where the logs will be pushed. If not given,
        a logger taking the name of the class and the module will be created.

    :param log_result: `bool`
        A flag to determine whether the results of the async operations should be logged or not.
        By default, False.

    :param log_level: `int`
        The logging level.
        By default, logging.DEBUG.

    :param log_time: `bool`
        Whether to log start and finish time.
        Default False.

    :return: `cls`
        The original class with wrapped coroutine functions that logs when called and possibly their results.
    """

    def decorator(cls: type) -> type:
        for attr in dir(cls):
            if attr.startswith("__"):
                continue

            value = getattr(cls, attr)

            if inspect.iscoroutinefunction(value):
                wrapped = log_function(
                    logger_name=logger_name if logger_name is not None else f"calls.{cls.__module__}.{cls.__name__}",
                    log_result=log_result,
                    log_level=log_level,
                    log_time=log_time
                )(value)

                setattr(cls, attr, wrapped)

        return cls

    return decorator
