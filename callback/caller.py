from abc import ABC, abstractmethod
from typing import Callable


class ICallbackCaller(ABC):
    @abstractmethod
    def call_callback(self, target: Callable[[], None]) -> None:
        raise NotImplementedError()
