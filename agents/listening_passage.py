import random
from langchain_core.prompts import PromptTemplate
from .base import BaseAgent
from llm_client import GoogleLLMClient
from config import GeminiModel


class ListeningPassageAgent(BaseAgent[str, str]):
    """
    주어진 시나리오 타입('academic' 또는 'conversation')에 대한 TOEFL 듣기 스크립트(str)를 생성하는 에이전트입니다.
    """

    def _initialize_agent(self):
        """프롬프트 템플릿과 LLM 클라이언트를 초기화합니다."""
        self.llm_client = GoogleLLMClient(
            model_name=GeminiModel.GEMINI_2_5_FLASH,
            temperature=0.8
        )

    def run(self, scenario_type: str = 'random') -> str:
        """
        시나리오 타입을 입력받아 듣기 스크립트를 생성합니다.

        Args:
            scenario_type (str): 'academic', 'conversation', 또는 'random' 중 하나.

        Returns:
            str: 생성된 TOEFL 듣기 스크립트.
        """
        if scenario_type == 'random':
            scenario_type = random.choice(['academic', 'conversation'])

        print(f"\n▶️ Generating listening script for scenario: '{scenario_type}'...")

        prompt_template = self._create_prompt_template(scenario_type)
        final_prompt = prompt_template.format()

        script = self.llm_client.invoke(final_prompt)
        print("✅ Script generated successfully.")
        return script

    def _create_prompt_template(self, scenario_type: str) -> PromptTemplate:
        """선택된 시나리오에 맞는 프롬프트 템플릿을 로드하고 생성합니다."""
        if scenario_type == 'academic':
            path = "prompts/listening/academic_passage.txt"
        elif scenario_type == 'conversation':
            path = "prompts/listening/campus_conversation_passage.txt"
        else:
            raise ValueError("Invalid scenario_type provided.")

        try:
            with open(path, "r", encoding="utf-8") as f:
                prompt_text = f.read()
            return PromptTemplate.from_template(prompt_text)
        except FileNotFoundError:
            raise FileNotFoundError(f"Instruction file not found at: {path}")
