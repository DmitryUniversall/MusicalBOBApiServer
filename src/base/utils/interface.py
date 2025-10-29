from abc import ABCMeta
from inspect import isabstract
from typing import Any, Optional


class InterfaceMeta(ABCMeta):
    def __new__(mcls, name: str, bases: tuple[type], namespace: dict[str, Any], **kwargs):
        _cls = super().__new__(mcls, name, bases, namespace, **kwargs)

        if isabstract(_cls):
            _cls._bind = None  # type: ignore
            _cls._bind_instance = None  # type: ignore

            _cls.bind_implementation = classmethod(mcls.__bind_implementation)  # type: ignore
            _cls.get_implementation = classmethod(mcls.__get_implementation)  # type: ignore

        return _cls

    @staticmethod
    def __bind_implementation[T](cls: type[T], impl_cls: type[T], impl: Optional[T] = None) -> None:
        if not isabstract(cls):
            raise TypeError(f"'{cls.__name__}' is not an abstract interface so it cannot have implementations")

        if isabstract(impl_cls):
            raise TypeError(f"'{impl_cls.__name__}' is a abstract interface so it cannot be implementation for {cls.__name__}")

        if cls._bind is not None:  # type: ignore
            raise TypeError(f"{cls.__name__}: Implementation for abstract interface can only be set once")

        cls._bind = impl_cls  # type: ignore
        if impl is not None:
            cls._bind_instance = impl  # type: ignore

    @staticmethod
    def __get_implementation[T](cls: type[T]) -> T:
        if cls._bind is None:  # type: ignore
            raise TypeError(f"{cls.__name__}: Implementation for abstract interface is not set")

        if cls._bind_instance is None:  # type: ignore
            cls._bind_instance = cls._bind()  # type: ignore

        return cls._bind_instance  # type: ignore
