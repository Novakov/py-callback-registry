from typing import Callable, List

from callback import callback_registry, ICallbackCaller


class MyClass(ICallbackCaller):
    def __init__(self) -> None:
        self.call_flags: List[int] = []

    @callback_registry
    def on_something(self) -> None:
        pass

    def method(self) -> None:
        self.on_something()

    def call_callback(self, f: Callable[[], None]) -> None:
        self.call_flags.append(2)
        f()


def test_custom_caller() -> None:
    flags = []
    obj = MyClass()

    def h(self: MyClass) -> None:
        flags.append(1)

    obj.on_something += h

    obj.method()

    assert flags == [1]
    assert obj.call_flags == [2]
