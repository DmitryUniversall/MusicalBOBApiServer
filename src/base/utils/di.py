from abc import ABC, abstractmethod
from functools import wraps
from types import FunctionType
from typing import Optional, Any, Callable, ParamSpec, TypeVar, cast, get_origin, get_args, Awaitable

P = ParamSpec("P")
R = TypeVar("R")


class Inject[T]:
    def __class_getitem__(cls, params: Any) -> tuple[type['Inject[T]'], type[T], Optional[str]]:
        if not isinstance(params, tuple):
            return cls, params, None
        if len(params) == 1:
            return cls, params[0], None
        if len(params) == 2:
            return cls, params[0], params[1]

        raise TypeError("Inject[...] accepts at most two parameters: type and optional tag")


class AbstractDependencyProvider[T: Any](ABC):
    __tag__: Optional[str] = None
    __access__: DIAccessModifier = DIAccessModifier.PUBLIC

    @property
    @abstractmethod
    def __provides_cls__(self) -> type[T]:
        ...


class DependencyProvider[T](ABC, AbstractDependencyProvider[T]):
    @abstractmethod
    def provide(self, **kwargs) -> T:
        ...


class AsyncDependencyProvider[T](ABC, AbstractDependencyProvider[T]):
    @abstractmethod
    async def provide(self, **kwargs) -> T:
        ...


class DependencyContainer:
    def __init__(self) -> None:
        self._providers: dict[tuple[type, str], DependencyProvider | AsyncDependencyProvider] = {}

    def inject(self, func: Callable[P, R]) -> Callable[P, R]:
        func = cast(FunctionType, func)

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            for name, type_ in func.__annotations__.items():
                if name == "return" or name in kwargs or get_origin(type_) is not Inject:
                    continue

                dependency_type, tag = get_args(type_)
                kwargs[name] = self.get(dependency_type)

            return func(*args, **kwargs)

        return wrapper

    def inject_async(self, coro: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        coro = cast(FunctionType, coro)

        @wraps(coro)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            for name, type_ in coro.__annotations__.items():
                if name == "return" or name in kwargs or get_origin(type_) is not Inject:
                    continue

                dependency_type, tag = get_args(type_)
                kwargs[name] = await self.get_async(dependency_type, tag=tag)

            return await coro(*args, **kwargs)

        return wrapper

    def provides[T](self, cls: type[T], tag: Optional[str] = None, provider_cls: type[AbstractDependencyProvider[T]] = AbstractDependencyProvider, **init_kwargs):
        def decorator(coro) -> AbstractDependencyProvider[T]:
            @wraps(coro)
            async def wrapper(provider_self: AbstractDependencyProvider, *args, **kwargs) -> T:
                return await coro(*args, **kwargs, provider=provider_self)

            provider = type(provider_cls.__name__, (provider_cls,), {
                "__provides_cls__": cls,
                "__tag__": tag,
                "provide": self.inject(wrapper)
            })

            return provider(**init_kwargs)

        return decorator

    def register_provider(self, provider: AbstractDependencyProvider) -> None:
        pass

    def bind[T](self, cls: type[T], impl_cls: type[T], impl: Optional[T] = None) -> None:
        bind_instance = impl

        def wrapper():
            nonlocal bind_instance

            if bind_instance is None:
                bind_instance = self.inject(impl_cls())

            return cls._bind_instance

        self.register_provider(self.provides(cls)(wrapper))

    async def get[T](self, cls: type[T], tag: Optional[str] = None) -> T:
        if (provider := self._providers.get(dependency_type)) is None:
            raise TypeError(f"Failed to inject '{name}' into '{func.__name__}': provider for type '{dependency_type.__name__}' is not defined")

        kwargs[name] = self.provider.provide()

    async def get_async[T](self, cls: type[T], tag: Optional[str] = None) -> T:
        pass
