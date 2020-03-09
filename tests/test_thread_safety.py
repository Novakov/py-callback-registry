from threading import Barrier, Semaphore, Thread

import pytest

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


@pytest.mark.parametrize('threads_count', [2, 5, 10, 15, 20, 50, 100, 500])  # type: ignore
def test_thread_safe_single_object(threads_count: int) -> None:
    for x in range(0, 100):
        o = MyClass()
        barrier = Barrier(threads_count)
        counter = Semaphore(0)

        def run(i: int) -> None:
            def clb(self: MyClass, a: int, b: bool) -> None:
                counter.release()

            barrier.wait()
            o.on_something2 += clb

        threads = [Thread(target=run, args=(x,)) for x in range(0, threads_count)]

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        o.method2()

        i = 0
        while counter.acquire(blocking=False):
            i += 1

        assert i == threads_count


@pytest.mark.parametrize('threads_count', [2, 5, 10, 15, 20, 50, 100, 500])  # type: ignore
def test_thread_safe_multiple_callbacks(threads_count: int) -> None:
    for x in range(0, 100):
        o = MyClass()
        barrier = Barrier(threads_count * 2)
        counter1 = Semaphore(0)
        counter2 = Semaphore(0)

        def run1(i: int) -> None:
            def clb(self: MyClass, a: int, b: bool) -> None:
                counter1.release()

            barrier.wait()
            o.on_something1 += clb

        def run2(i: int) -> None:
            def clb(self: MyClass, a: int, b: bool) -> None:
                counter2.release()

            barrier.wait()
            o.on_something2 += clb

        threads1 = [Thread(target=run1, args=(x,)) for x in range(0, threads_count)]
        threads2 = [Thread(target=run2, args=(x,)) for x in range(0, threads_count)]

        for t in threads1:
            t.start()

        for t in threads2:
            t.start()

        for t in threads1:
            t.join()

        for t in threads2:
            t.join()

        o.method2()
        o.method1()

        i = 0
        while counter1.acquire(blocking=False):
            i += 1

        assert i == threads_count

        i = 0
        while counter2.acquire(blocking=False):
            i += 1

        assert i == threads_count
