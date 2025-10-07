from langchain_core.prompts import PromptTemplate

from .base import BaseAgent
from llm_client import GoogleLLMClient
from config import GeminiModel


class QuestionThoughtProcessAgent(BaseAgent[dict, str]):
    """
    주어진 지문과 질문 JSON을 바탕으로,
    질문 생성 과정의 "사고 과정(Thought Process)"을 생성하는 헬퍼 에이전트입니다.
    """

    def _initialize_agent(self):
        """사고 과정 생성을 위한 LLM 클라이언트와 프롬프트 템플릿을 초기화합니다."""
        self.llm_client = GoogleLLMClient(
            model_name=GeminiModel.GEMINI_2_5_FLASH,
            temperature=0.5,
        )
        self.prompt_template = self._load_prompt_template()

    def run(self, inputs: dict) -> str:
        """
        사고 과정 텍스트를 생성합니다.

        Args:
            inputs (dict): 'passage'와 'json_output' 키를 포함하는 딕셔너리.

        Returns:
            str: LLM이 생성한 사고 과정 텍스트.
        """
        print("\n▶️ Generating thought process for the question set...")

        passage = inputs.get("passage")
        json_output = inputs.get("json_output")

        if not passage or not json_output:
            raise ValueError(
                "Inputs dictionary must contain 'passage' and 'json_output' keys."
            )

        final_prompt = self.prompt_template.format(
            passage=passage, json_output=json_output
        )

        thought_process = self.llm_client.invoke(final_prompt)
        print("✅ Thought process generated successfully.")
        return thought_process

    def _load_prompt_template(self) -> PromptTemplate:
        """사고 과정 생성을 위한 프롬프트 템플릿을 로드합니다."""
        try:
            with open(
                "prompts/reading/question_thought_process_instruction.txt",
                "r",
                encoding="utf-8",
            ) as f:
                prompt_text = f.read()

            return PromptTemplate(
                template=prompt_text,
                input_variables=["passage", "json_output"],
            )
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Instruction file not found: {e}")


class PassageThoughtProcessAgent(BaseAgent[dict, str]):
    """
    주어진 토픽과 최종 지문을 바탕으로,
    지문 생성 과정의 "사고 과정(Thought Process)"을 생성하는 헬퍼 에이전트입니다.
    """

    def _initialize_agent(self):
        """사고 과정 생성을 위한 LLM 클라이언트와 프롬프트 템플릿을 초기화합니다."""
        self.llm_client = GoogleLLMClient(
            model_name=GeminiModel.GEMINI_2_5_FLASH,
            temperature=0.5,
        )
        self.prompt_template = self._load_prompt_template()

    def run(self, inputs: dict) -> str:
        """
        사고 과정 텍스트를 생성합니다.

        Args:
            inputs (dict): 'topic'과 'final_passage' 키를 포함하는 딕셔너리.

        Returns:
            str: LLM이 생성한 사고 과정 텍스트.
        """
        print("\n▶️ Generating thought process for the passage...")

        topic = inputs.get("topic")
        final_passage = inputs.get("final_passage")

        if not topic or not final_passage:
            raise ValueError(
                "Inputs dictionary must contain 'topic' and 'final_passage' keys."
            )

        final_prompt = self.prompt_template.format(
            topic=topic, final_passage=final_passage
        )

        thought_process = self.llm_client.invoke(final_prompt)
        print("✅ Thought process generated successfully.")
        return thought_process

    def _load_prompt_template(self) -> PromptTemplate:
        """사고 과정 생성을 위한 프롬프트 템플릿을 로드합니다."""
        try:
            with open(
                "prompts/reading/passage_thought_process_instruction.txt",
                "r",
                encoding="utf-8",
            ) as f:
                prompt_text = f.read()

            return PromptTemplate(
                template=prompt_text,
                input_variables=["topic", "final_passage"],
            )
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Instruction file not found: {e}")
