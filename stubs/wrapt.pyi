from typing import Any, Callable, TypeVar

_T = TypeVar('_T', bound=Callable[..., Any])


def synchronized(wrapped: _T) -> _T: ...
