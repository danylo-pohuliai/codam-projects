from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._storage: list[tuple[int, str]] = []
        self._counter: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool: ...

    @abstractmethod
    def ingest(self, data: Any) -> None: ...

    def output(self) -> tuple[int, str]:
        if not self._storage:
            raise IndexError("No data available to output")
        return self._storage.pop(0)

    def get_counter(self) -> int:
        return self._counter

    def get_storage(self) -> list[tuple[int, str]]:
        return self._storage


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if type(data) is int or type(data) is float:
            return True
        if type(data) is list:
            for d in data:
                if type(d) is not int and type(d) is not float:
                    return False
            return True
        return False

    def ingest(
            self,
            data: int | float | list[int] | list[float]
            | list[int | float]
            ) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")

        if type(data) is list:
            for d in data:
                self._storage.append((self._counter, str(d)))
                self._counter += 1
        else:
            self._storage.append((self._counter, str(data)))
            self._counter += 1


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if type(data) is str:
            return True
        if type(data) is list:
            for d in data:
                if type(d) is not str:
                    return False
            return True
        return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")

        if isinstance(data, list):
            for d in data:
                self._storage.append((self._counter, d))
                self._counter += 1
        else:
            self._storage.append((self._counter, data))
            self._counter += 1


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if type(data) is dict:
            for key, value in data.items():
                if type(key) is not str or type(value) is not str:
                    return False
            return True

        if type(data) is list:
            for d in data:
                if type(d) is not dict:
                    return False

                for key, value in d.items():
                    if type(key) is not str or type(value) is not str:
                        return False
            return True
        return False

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")

        if isinstance(data, list):
            for d in data:
                if "log_level" in d and "log_message" in d:
                    formatted_log = f"{d['log_level']}: {d['log_message']}"
                else:
                    formatted_log = str(d)
                self._storage.append((self._counter, formatted_log))
                self._counter += 1
        else:
            if "log_level" in data and "log_message" in data:
                formatted_log = f"{data['log_level']}: {data['log_message']}"
            else:
                formatted_log = str(data)

            self._storage.append((self._counter, formatted_log))
            self._counter += 1


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for item in stream:
            handled = False
            for proc in self._processors:
                if proc.validate(item):
                    proc.ingest(item)
                    handled = True
                    break

            if not handled:
                print(
                    "DataStream error - Can't process "
                    f"element in stream: {item}"
                    )

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data\n")
            return
        for proc in self._processors:
            name = type(proc).__name__.replace("Processor", " Processor")

            total = proc.get_counter()
            remaining = len(proc.get_storage())
            print(
                f"{name}: total {total} items processed, "
                f"remaining {remaining} on processor"
                )
        print("")


if __name__ == "__main__":
    print("=== Code Nexus - Data Stream ===\n")
    print("Initialize Data Stream...")

    stream = DataStream()
    stream.print_processors_stats()

    print("Registering Numeric Processor\n")
    num_proc = NumericProcessor()
    stream.register_processor(num_proc)

    batch = [
        'Hello world',
        [3.14, -1, 2.71],
        [
            {'log_level': 'WARNING',
             'log_message': 'Telnet access! Use ssh instead'},
            {'log_level': 'INFO', 'log_message': 'User wil is connected'}
        ],
        42,
        ['Hi', 'five']
    ]

    print(f"Send first batch of data on stream: {batch}")
    stream.process_stream(batch)
    stream.print_processors_stats()

    print("Registering other data processors")
    text_proc = TextProcessor()
    log_proc = LogProcessor()
    stream.register_processor(text_proc)
    stream.register_processor(log_proc)

    print("Send the same batch again")
    stream.process_stream(batch)
    stream.print_processors_stats()

    print(
        "Consume some elements from the data processors: "
        "Numeric 3, Text 2, Log 1"
        )
    for _ in range(3):
        num_proc.output()
    for _ in range(2):
        text_proc.output()
    for _ in range(1):
        log_proc.output()

    stream.print_processors_stats()
