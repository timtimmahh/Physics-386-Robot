from multiprocessing import Process
from typing import Callable


def start_thread(target, value=...):
    if value:
        value = value if isinstance(value, list) else [value]
    if callable(target):
        return __start_thread__(target=target, value=value)
    else:
        return [__start_thread__(target=t, value=value) for t in target]


def __start_thread__(target: Callable, value):
    if value:
        proc = Process(target=target, args=value)
    else:
        proc = Process(target=target)
    proc.start()
    return proc
