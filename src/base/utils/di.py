from abc import ABC, abstractmethod
from enum import Enum
from types import FunctionType
from typing import Optional, Any, Callable, Awaitable, Self, cast, get_origin, get_args

type AnyFunc[T] = Callable[..., T]
type AnyCoro[T] = Callable[..., Awaitable[T]]

type GenericDecorator[T] = Callable[[AnyFunc[T]], AnyFunc[T]]
type GenericCoroDecorator[T] = Callable[[AnyCoro[T]], AnyCoro[T]]

type DefaultProvider = DependencyProvider | AsyncDependencyProvider


class DIAccess(Enum):
    PUBLIC = 0
    PRIVATE = 1


class Inject[T: Any]:
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
    __access__: DIAccess = DIAccess.PUBLIC

    @property
    @abstractmethod
    def __provides_cls__(self) -> type[T]:
        ...

    @classmethod
    def binds(
            cls: type[Self],
            interface_cls: type[T],
            impl_cls: type[T],
            impl: Optional[T] = None,
            tag: Optional[str] = None,
            use_containers: Optional[tuple['DependencyContainer']] = None
    ) -> type[Self]:
        _bind_instance: Optional[T] = impl

        def wrapper(*args, **kwargs) -> T:
            nonlocal _bind_instance

            if _bind_instance is None:
                _bind_instance = impl_cls(*args, **kwargs)

            return _bind_instance

        return cls.provides(interface_cls, tag, use_containers)(wrapper)

    @classmethod
    def provides(
            cls: type[Self],
            interface_cls: type[T],
            tag: Optional[str] = None,
            use_containers: Optional[tuple['DependencyContainer']] = None
    ) -> Callable[[AnyFunc[T]], type[Self]]:
        def decorator(func: AnyFunc[T]) -> type[Self]:
            def wrapper(provider_self: Self, *args, **kwargs) -> T:
                return func(*args, **kwargs, provider=provider_self)

            if use_containers is not None:
                for container in use_containers:
                    wrapper = container.inject(raise_error=False)(wrapper)

            return type(f"{cls.__name__}Provider", (cls,), {  # type: ignore
                "__provides_cls__": interface_cls,
                "__tag__": tag,
                "provide": wrapper
            })

        return decorator


class DependencyProvider[T: Any](AbstractDependencyProvider[T]):
    @abstractmethod
    def provide(self, *args, **kwargs) -> T:
        pass

    def wrap_provide(self, func: GenericDecorator[T]) -> None:
        self.provide = func(self.provide)  # type: ignore [method-assign, assignment]


class AsyncDependencyProvider[T: Any](AbstractDependencyProvider[T]):
    @classmethod
    def provides_async(
            cls: type[Self],
            interface_cls: type[T],
            tag: Optional[str] = None,
            use_containers: Optional[tuple['DependencyContainer']] = None
    ) -> Callable[[AnyCoro[T]], type[Self]]:
        def decorator(coro: AnyCoro[T]) -> type[Self]:
            async def wrapper(provider_self: Self, *args, **kwargs) -> T:
                return await coro(*args, **kwargs, provider=provider_self)

            if use_containers is not None:
                for container in use_containers:
                    wrapper = container.inject_async(raise_error=False)(wrapper)  # type: ignore [assignment]

            return type(f"{cls.__name__}Provider", (cls,), {  # type: ignore
                "__provides_cls__": interface_cls,
                "__tag__": tag,
                "provide_async": wrapper
            })

        return decorator

    def wrap_provide(self, coro: GenericCoroDecorator[T]) -> None:
        self.provide = coro(self.provide)  # type: ignore [method-assign, assignment]

    @abstractmethod
    async def provide_async(self, *args, **kwargs) -> T:
        pass


class DependencyContainer:
    def __init__(self) -> None:
        self._providers: dict[tuple[type, Optional[str]], DefaultProvider] = {}
        self._init_providers()

    def _init_providers(self) -> None:
        for name, attr in self.__class__.__dict__.items():
            if not isinstance(attr, type) or not issubclass(attr, (DependencyProvider | AsyncDependencyProvider)):
                continue

            provider = attr()
            self._providers[(attr.__provides_cls__, attr.__tag__)] = provider  # type: ignore

            if isinstance(attr, DependencyProvider):
                provider.wrap_provide(self._inject_private(raise_error=False))
            else:
                provider.wrap_provide(self._inject_private_async(raise_error=False))

    def _inject[T](self, *, access: DIAccess, raise_error: bool = False) -> GenericDecorator:
        def decorator(coro: AnyFunc[T]) -> AnyFunc[T]:
            def wrapper(*args, **kwargs) -> T:
                pass

            return wrapper

        return decorator

    def _inject_async[T](self, *, access: DIAccess, raise_error: bool = False) -> GenericCoroDecorator:
        def decorator(coro: AnyCoro[T]) -> AnyCoro[T]:
            coro = cast(FunctionType, coro)

            async def wrapper(*args, **kwargs) -> T:
                for name, type_ in coro.__annotations__.items():
                    if get_origin(type_) is not Inject or name == "return" or name in kwargs:
                        continue

                    dependency_type, tag = get_args(type_)
                    kwargs[name] = await self._get_async(dependency_type, access=access, tag=tag, raise_error=raise_error)

                return await coro(*args, **kwargs)

            return wrapper

        return decorator

    def _inject_private(self, *, raise_error: bool = True) -> GenericDecorator:
        return self._inject(access=DIAccess.PRIVATE, raise_error=raise_error)

    def _inject_private_async(self, *, raise_error: bool = True) -> GenericCoroDecorator:
        return self._inject_async(access=DIAccess.PRIVATE, raise_error=raise_error)

    def _get_provider[T](self, dependency_type: type[T], tag: Optional[str] = None, raise_error: bool = True) -> DefaultProvider:
        pass

    def _get[T](self, dependency_type: type[T], *, access: DIAccess, tag: Optional[str] = None, raise_error: bool = True) -> T:
        pass

    def _get_async[T](self, dependency_type: type[T], *, access: DIAccess, tag: Optional[str] = None, raise_error: bool = True) -> T:
        pass

    def get[T](self, dependency_type: type[T], tag: Optional[str] = None, raise_error: bool = True) -> T:
        pass

    async def get_async[T](self, dependency_type: type[T], tag: Optional[str] = None, raise_error: bool = True) -> T:
        pass

    def inject(self, *, raise_error: bool = True) -> GenericDecorator:
        return self._inject(access=DIAccess.PUBLIC, raise_error=raise_error)

    def inject_async(self, *, raise_error: bool = True) -> GenericCoroDecorator:
        return self._inject_async(access=DIAccess.PUBLIC, raise_error=raise_error)
