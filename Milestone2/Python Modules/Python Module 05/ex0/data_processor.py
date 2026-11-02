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


if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===")
    num_proc = NumericProcessor()
    text_proc = TextProcessor()
    log_proc = LogProcessor()
    print("\nTesting Numeric Processor...")
    print(f" Trying to validate input '42': {num_proc.validate(42)}")
    print(f" Trying to validate input 'Hello': {num_proc.validate("Hello")}")
    print(" Test invalid ingestion of string 'foo' without prior validation:")
    try:
        num_proc.ingest("foo")
    except Exception as e:
        print(f" Got exception: {e}")
    valid_nums = [1, 2, 3, 4, 5]
    print(f" Processing data: {valid_nums}")
    num_proc.ingest(valid_nums)
    print(" Extracting 3 values...")
    for _ in range(3):
        count, val = num_proc.output()
        print(f" Numeric value {count}: {val}")

    print("\nTesting Text Processor...")
    print(f" Trying to validate input '42': {text_proc.validate(42)}")
    valid_texts = ['Hello', 'Nexus', 'World']
    print(f" Processing data: {valid_texts}")
    text_proc.ingest(valid_texts)
    print(" Extracting 1 value...")
    count, val = text_proc.output()
    print(f" Text value {count}: {val}")

    print("\nTesting Log Processor...")
    print(f" Trying to validate input 'Hello': {log_proc.validate('Hello')}")

    valid_logs = [
        {'log_level': 'NOTICE', 'log_message': 'Connection to server'},
        {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}
    ]
    print(f" Processing data: {valid_logs}")
    log_proc.ingest(valid_logs)

    print(f" Extracting {len(valid_logs)} values...")
    for _ in range(len(valid_logs)):
        count, val = log_proc.output()
        print(f" Log entry {count}: {val}")
