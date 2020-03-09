from callback import callback_registry


class MyClass:
    def method1(self) -> None:
        self.on_something1(10, False)

    def method2(self) -> None:
        self.on_something2(10, True)

    @callback_registry
    def on_something1(self, a: int, b: bool) -> None:
        pass

    @callback_registry
    def on_something2(self, a: int, b: bool) -> None:
        pass


def test_register_and_call_callback() -> None:
    flags = []

    obj1 = MyClass()

    def h1(owner: MyClass, a: int, b: bool) -> None:
        flags.append((1, a, b))

    def h2(owner: MyClass, a: int, b: bool) -> None:
        flags.append((2, a, b))

    obj1.on_something2 += h1

    obj2 = MyClass()
    obj2.on_something2 += h2

    obj1.method2()
    obj2.method2()

    assert flags == [(1, 10, True), (2, 10, True)]


def test_unregister_callback() -> None:
    flags = []
    obj = MyClass()

    def clb(owner: MyClass, a: int, b: bool) -> None:
        flags.append(1)

    obj.on_something1 += clb

    obj.method1()

    obj.on_something1 -= clb

    obj.method1()

    assert flags == [1]
