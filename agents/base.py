from abc import ABC, abstractmethod
from typing import TypeVar, Generic

# 제네릭 타입을 위한 TypeVar 정의
InputType = TypeVar('InputType')
OutputType = TypeVar('OutputType')

class BaseAgent(ABC, Generic[InputType, OutputType]):
    """
    This class is base class for other agent classes
    """

    def __init__(self):
        """Initial common methods, such as LLM client."""
        print(f"Initializing {self.__class__.__name__}...")
        self._initialize_agent()
        print(f"✅ {self.__class__.__name__} initialized.")

    @abstractmethod
    def _initialize_agent(self):
        """
        This is abstract methods to load initial logic, such as prompt loading and etc.
        It must be implemented in the subclass.
        """
        pass

    @abstractmethod
    def run(self, inputs: InputType) -> OutputType:
        """

        모든 에이전트의 메인 실행 메서드입니다.
        입력을 받아 출력을 반환하는 공통 인터페이스 역할을 합니다.
        하위 클래스에서 반드시 구현해야 합니다.
        """
        pass