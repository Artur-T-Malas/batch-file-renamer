import sys
from typing import Callable
import traceback

from PySide6.QtCore import (
    Signal,
    Slot,
    QRunnable,
    QObject
)


class WorkerSignals(QObject):
    """Represents signals from a running worker thread.

    Based on https://www.pythonguis.com/tutorials/multithreading-pyside6-applications-qthreadpool/

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc())

    result
        object data returned from processing, anything

    progress
        float indicating task progress
    """

    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(float)


class Worker(QRunnable):
    """Represents a worker thread.

    Inherits from QRunnable to handle thread setup, signals and clean-up.
    """

    def __init__(self, fn: Callable, *args, **kwargs) -> None:
        """Initialise the worker thread.

        Args:
            fn (Callable): The function to be executed.
            args: The arguments to be passed to `fn`.
            kwargs: The keyword arguments to be passed to `fn`.
        """
        super().__init__()
        self.fn: Callable = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.kwargs["progress_callback"] = self.signals.progress

    @Slot()
    def run(self) -> None:
        """Run the runner function with passed args, kwargs."""

        try:
            result = self.fn(*self.args, **self.kwargs)

        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))

        else:
            self.signals.result.emit(result)

        self.signals.finished.emit()
