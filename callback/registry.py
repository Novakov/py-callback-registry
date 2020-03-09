from typing import List, Callable, Dict, Any, Tuple, TypeVar, Generic

from wrapt import synchronized
from .caller import ICallbackCaller

T = TypeVar('T', bound=Callable[..., None])


class CallbackRegistry(Generic[T]):
    def __init__(self, owner: object):
        self._targets: List[T] = []
        self._owner = owner
        if isinstance(self._owner, ICallbackCaller):
            self._call = lambda args, kwargs: self._owner.call_callback(lambda: self._call_callbacks(args, kwargs))
        else:
            self._call = self._call_callbacks

    @synchronized
    def __iadd__(self, other: T) -> 'CallbackRegistry[T]':
        self._targets.append(other)
        return self

    @synchronized
    def __isub__(self, other: T) -> 'CallbackRegistry[T]':
        self._targets.remove(other)
        return self

    @synchronized
    def _get_targets(self) -> List[T]:
        return list(self._targets)

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        self._call(args, kwargs)  # type: ignore

    def _call_callbacks(self, args: Any, kwargs: Dict[str, Any]) -> None:
        targets = self._get_targets()
        for t in targets:
            t(self._owner, *args, **kwargs)

    def __str__(self) -> str:
        return f'Callback: {len(self._targets)} callbacks'
