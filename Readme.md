Callbacks registry in Python
---

# Usage


Define class with instance methods marked with `callback.callback_regisry` decorator:

```python
from callback import callback_registry


class SomeClass:
    @callback_registry
    def on_something(self, arg1: int, arg2: bool) -> None:
        pass

    def method(self, arg: int) -> None:
        self.on_something(arg, arg == 42)
```

Each time `SomeClass.on_something` is called all registered handlers will be invoked. Handlers can be registered using `+=` operator and removed by `-=` operator:

```python
obj = SomeClass()

def handler(owner: SomeClass, arg1: int, arg2: bool) -> None:
    print('Handler called')

# register handler
obj.on_something += handler

print('Calling...')
obj.method(42)

# remove handler
obj.on_something -= handler
```

It is possible to register many handlers for single callback, they will be called in order. Any exception raised by single handler will be propagated and will prevent remaining handlers from running.

# Additional features
## Custom call wrapper
In some cases it is useful to execute callbacks in specific way, e.g. execute them asynchronously in some kind of work queue. Each class can provide custom caller for callbacks which will be used automatically, class have to inherit from `callback.ICallbackCaller` and implement `call_callback` method.

```python
from callback import ICallbackCaller, callback_registry
from typing import Callable
from work_queue import post_to_queue

class SomeClass(ICallbackCaller):
    @callback_registry
    def on_something(self, arg1: int, arg2: bool) -> None:
        pass

    def method(self, arg: int) -> None:
        self.on_something(arg, arg == 42)

    def call_callback(self, target: Callable[[], None]) -> None:
        post_to_queue(lambda: target())
```

# mypy integration
It is not possible to implement strict typing for callback registry using pure Python type hints. For mypy users this package includes plugin that provides support for type checking callbacks. 

Plugin can be enabled by adding following snippet to mypy config file:
```
[mypy]
plugins = callback._mypy.plugin
```
