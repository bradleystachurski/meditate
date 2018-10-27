from abc import ABC, abstractmethod
from threading import Thread
from typing import Callable


class Startable:
    def __init__(self):
        self._started = False

    def is_started(self) -> bool:
        return self._started

    def start(self) -> bool:
        if self._started:
            return False
        self._started = True
        return True

    def stop(self) -> bool:
        if not self._started:
            return False
        self._started = False
        return True


class StartableBackgroundThread(ABC, Startable):
    """Base class that creates a Thread on start() that runs the background task returned
    by _get_background_task_function(). This function will only be called once.

    Attributes:
        _thread: The handle for the Thread used for the background task
    """
    def __init__(self):
        super().__init__()
        self._thread = None

    def start(self) -> bool:
        if super().start():
            self._thread = Thread(target=self._get_background_task_function())
            self._thread.start()
            return True
        return False

    def stop(self) -> bool:
        if super().stop():
            self._thread.join(.05)
            return True
        return False

    @abstractmethod
    def _get_background_task_function(self) -> Callable:
        """The abstract method that is called to get the function the Thread should run"""
        pass

