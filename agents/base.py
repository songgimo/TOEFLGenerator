from abc import ABC, abstractmethod
from typing import TypeVar, Generic
import os

InputType = TypeVar("InputType")
OutputType = TypeVar("OutputType")


class BaseAgent(ABC, Generic[InputType, OutputType]):
    def __init__(self):
        print(f"Initializing {self.__class__.__name__}...")
        self._initialize_agent()
        print(f"✅ {self.__class__.__name__} initialized.")

    @abstractmethod
    def _initialize_agent(self):
        pass

    @abstractmethod
    def run(self, inputs: InputType) -> OutputType:
        pass

    def _read_file(self, path: str) -> str:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Cannot find a prompt file. Path is invalid: {path}"
            )

    def _load_examples(self, examples_path: str) -> list[dict]:
        examples = []
        print(f"Loading examples from: {examples_path}")
        for example_dir in sorted(os.listdir(examples_path)):
            full_dir_path = os.path.join(examples_path, example_dir)

            if os.path.isdir(full_dir_path):
                try:
                    example = {
                        "topic": self._read_file(os.path.join(full_dir_path, "topic.txt")),
                        "thought_process": self._read_file(os.path.join(full_dir_path, "thought_process.txt")),
                        "output": self._read_file(os.path.join(full_dir_path, "output.txt")),
                    }
                    examples.append(example)
                except FileNotFoundError as e:
                    print(f"Warning: Skipping directory {example_dir} because a required file is missing: {e}")

        print(f"✅ Loaded {len(examples)} few-shot examples.")
        return examples
