from threading import Lock
from typing import Any, TypeVar, Callable, cast, Optional
from .registry import CallbackRegistry

meta_lock = Lock()


def get_safe_lock(owner: Any, lock_name: str, parent_lock: Lock) -> Lock:
    lock: Optional[Lock] = vars(owner).get(lock_name, None)
    if lock is not None:
        return lock

    with parent_lock:
        lock = vars(owner).get(lock_name, None)
        if lock is None:
            lock = Lock()
            setattr(owner, lock_name, lock)
        return lock


T = TypeVar('T', bound=Callable[..., None])


def callback_registry(f: T) -> CallbackRegistry[T]:
    callback_name = f.__name__

    def get_registry(owner: Any) -> CallbackRegistry[T]:
        registry = getattr(owner, '__callbacks', {}).get(callback_name, None)
        if registry is not None:
            return cast(CallbackRegistry[T], registry)

        callbacks_class_lock = get_safe_lock(owner.__class__, '__callbacks_class_lock', meta_lock)
        callbacks_lock = get_safe_lock(owner, '__callbacks_lock', callbacks_class_lock)

        with callbacks_lock:
            if not hasattr(owner, '__callbacks'):
                registry = CallbackRegistry(owner)
                setattr(owner, '__callbacks', {callback_name: registry})
            else:
                if f.__name__ in owner.__callbacks:
                    registry = owner.__callbacks[callback_name]
                else:
                    registry = CallbackRegistry(owner)
                    owner.__callbacks[callback_name] = registry

        return cast(CallbackRegistry[T], registry)

    def set_registry(owner: Any, new_value: Any) -> None:
        pass

    return cast(CallbackRegistry[T], property(fget=get_registry, fset=set_registry))
