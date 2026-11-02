from abc import ABC, abstractmethod
from typing import Any, Protocol


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


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None: ...


class CSVExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        if not data:
            return
        values = []
        for item in data:
            values.append(item[1])
        print("CSV Output:")
        print(",".join(values))


class JSONExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        if not data:
            return

        print("JSON Output:")
        json_pairs = []
        for count, value in data:
            clean_value = value.replace('"', '\\"')
            json_pairs.append(f'"item_{count}": "{clean_value}"')

        json_string = "{" + ", ".join(json_pairs) + "}"
        print(json_string)


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

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for proc in self._processors:
            collected_data: list[tuple[int, str]] = []
            for _ in range(nb):
                try:
                    item = proc.output()
                    collected_data.append(item)
                except IndexError:
                    break

            if collected_data:
                plugin.process_output(collected_data)


if __name__ == "__main__":
    print("=== Code Nexus - Data Pipeline ===\n")
    print("Initialize Data Stream...\n")

    stream = DataStream()
    stream.print_processors_stats()

    print("Registering Processors\n")
    num_proc = NumericProcessor()
    text_proc = TextProcessor()
    log_proc = LogProcessor()

    stream.register_processor(num_proc)
    stream.register_processor(text_proc)
    stream.register_processor(log_proc)

    batch1 = [
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

    print(f"Send first batch of data on stream: {batch1}\n")
    stream.process_stream(batch1)
    stream.print_processors_stats()

    print("Send 3 processed data from each processor to a CSV plugin:")
    csv_plugin = CSVExportPlugin()
    stream.output_pipeline(3, csv_plugin)
    stream.print_processors_stats()

    batch2 = [
        21,
        ['I love AI', 'LLMs are wonderful', 'Stay healthy'],
        [
            {'log_level': 'ERROR', 'log_message': '500 server crash'},
            {'log_level': 'NOTICE',
             'log_message': 'Certificate expires in 10 days'}
        ],
        [32, 42, 64, 84, 128, 168],
        'World hello'
    ]

    print(f"Send another batch of data: {batch2}\n")
    stream.process_stream(batch2)
    stream.print_processors_stats()

    print("Send 5 processed data from each processor to a JSON plugin:")
    json_plugin = JSONExportPlugin()
    stream.output_pipeline(5, json_plugin)
    print("")
    stream.print_processors_stats()
