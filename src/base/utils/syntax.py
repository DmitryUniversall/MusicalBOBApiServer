import functools
import inspect
import logging
import warnings
from typing import Callable, Any

from src.base.exceptions.generics import NoneObjectError

_logger = logging.getLogger(__name__)


class ValueWrapper[T: Any]:
    def __init__(self, value: T) -> None:
        self._value = value

    def __repr__(self):
        return f"Wrapper({self.value!r})"

    @property
    def value(self) -> T:
        return self._value

    def also(self, func: Callable[[T], None]) -> 'ValueWrapper[T]':
        func(self._value)
        return self

    def also_if(self, func: Callable[[T], None], *, check: Callable[[T], bool]) -> 'ValueWrapper[T]':
        if check(self._value):
            func(self._value)

        return self

    def then[U: Any](self, func: Callable[[T], U]) -> 'ValueWrapper[U]':
        return ValueWrapper[U](func(self._value))

    def let[U: Any](self, func: Callable[[T], U]) -> U:
        return func(self._value)

    def as_[U: Any](self, type_: type[U]) -> 'ValueWrapper[U]':
        return self.let(type_)


def default_any[_T](
        value: _T | None,
        *defaults: *tuple[_T, ...]
) -> _T:
    """
    Returns value if value is not None, in other case returns first not-None default

    :param value: `_T | None`
        Initial value

    :param defaults: `*tuple[_T, ...]`
        Default values

    :return: `_T`
        Returns value if value is not None, in other case returns first not-None default

    :raises:
        :raise NoneObjectError: If all default values are None
    """

    if value is not None:
        return value

    for default_value in defaults:
        if default_value is not None:
            return default_value

    raise NoneObjectError("All default values are None")


def deprecated(
        reason: str | type | Callable,
        warning_format: str = "Called deprecated {kind} {name}: {reason}"
):
    """
    Decorator function to mark a function or class as deprecated and issue a warning when it is called.

    :param reason: `str | type | Callable`
        The reason for deprecation, or a class/function to deprecate.

    :param warning_format: `str`
        The format string for the deprecation warning message.

    :return: `Callable`
        A decorated function or class.

    :raises:
        :raise TypeError: If the provided 'reason' argument is of an unsupported type.
    """

    def decorator(func):
        @functools.wraps(func)
        def new_func(*args, **kwargs):
            name = func.__name__
            kind = 'class' if inspect.isclass(func) else 'function'
            msg = reason if isinstance(reason, str) else f"{kind} is deprecated"

            warnings.simplefilter('always', DeprecationWarning)
            warnings.warn(
                message=warning_format.format(kind=kind, name=name, reason=msg),
                category=DeprecationWarning,
                stacklevel=2
            )
            warnings.simplefilter('default', DeprecationWarning)

            return func(*args, **kwargs)

        return new_func

    if isinstance(reason, str):
        return decorator
    elif isinstance(reason, type) or callable(reason):
        return decorator(reason)
    else:
        raise TypeError(repr(type(reason)))
