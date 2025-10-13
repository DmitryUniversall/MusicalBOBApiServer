from abc import ABCMeta
from inspect import isabstract
from typing import Any


class InterfaceMeta(ABCMeta):
    def __new__(mcls, name: str, bases: tuple[type], namespace: dict[str, Any], **kwargs):
        _cls = super().__new__(mcls, name, bases, namespace, **kwargs)

        if isabstract(_cls):
            _cls._bind = None
            _cls._bind_instance = None

            _cls.bind_implementation = classmethod(mcls.__bind_implementation)
            _cls.get_implementation = classmethod(mcls.__get_implementation)

        return _cls

    @staticmethod
    def __bind_implementation[T](cls: type[T], impl_cls: type[T]) -> None:
        if not isabstract(cls):
            raise TypeError(f"'{cls.__name__}' is not an abstract interface so it cannot have implementations")

        if isabstract(impl_cls):
            raise TypeError(f"'{impl_cls.__name__}' is a abstract interface so it cannot be implementation for {cls.__name__}")

        if cls._bind is not None:
            raise TypeError(f"{cls.__name__}: Implementation for abstract interface can only be set once")

        cls._bind = impl_cls

    @staticmethod
    def __get_implementation[T](cls: type[T]) -> T:
        if cls._bind is None:
            raise TypeError(f"{cls.__name__}: Implementation for abstract interface is not set")

        if cls._bind_instance is None:
            cls._bind_instance = cls._bind()

        return cls._bind_instance
