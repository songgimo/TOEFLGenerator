import os
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from .base import BaseAgent
from llm_client import GoogleLLMClient
from config import GeminiModel, BaseQuestionSet


class ReadingQuestionAgent(BaseAgent[str, BaseQuestionSet]):
    """
    주어진 지문(str)에 대한 TOEFL 질문 세트(BaseQuestionSet)를 생성하는 에이전트입니다.
    """

    def _initialize_agent(self):
        """질문 생성을 위한 LLM 클라이언트, 파서, 프롬프트 템플릿을 초기화합니다."""
        self.llm_client = GoogleLLMClient(
            model_name=GeminiModel.GEMINI_2_5_FLASH,
            temperature=0.7,
        )
        self.parser = JsonOutputParser(pydantic_object=BaseQuestionSet)
        self.prompt_template = self._create_few_shot_prompt()

    def run(self, passage: str) -> BaseQuestionSet:
        """
        지문을 입력받아 구조화된 질문 세트를 생성하고 반환합니다.

        Args:
            passage (str): 질문을 생성할 기반이 되는 TOEFL 지문.

        Returns:
            BaseQuestionSet: 생성된 질문들이 담긴 Pydantic 모델 객체.
        """
        print("\n▶️ Generating questions for the passage...")

        final_prompt = self.prompt_template.format(passage=passage)
        llm_output = self.llm_client.invoke(final_prompt)

        question_set = self.parser.parse(llm_output)

        print("✅ Questions generated successfully.")
        return question_set

    # --- 내부 헬퍼 메서드들 ---

    def _create_few_shot_prompt(self) -> FewShotPromptTemplate:
        """Few-Shot 프롬프트 템플릿을 생성합니다."""
        examples = self._load_examples("prompts/reading/question_examples")

        example_prompt = PromptTemplate(
            template="Passage:\n{passage}\n\nJSON Output:\n{output}",
            input_variables=["passage", "output"],
        )

        prefix = self._read_file("prompts/reading/question_instruction.txt")
        prefix = prefix.replace(
            "{format_instructions}",
            self.parser.get_format_instructions()
        )

        suffix = "Passage:\n{passage}\n\nJSON Output:"

        return FewShotPromptTemplate(
            examples=examples,
            example_prompt=example_prompt,
            prefix=prefix,
            suffix=suffix,
            input_variables=["passage"],
            example_separator="\n\n---\n\n"
        )

    def _load_examples(self, examples_path: str) -> list[dict]:
        """질문 생성 예제를 로드합니다."""
        examples = []
        for example_dir in sorted(os.listdir(examples_path)):
            full_dir_path = os.path.join(examples_path, example_dir)
            if os.path.isdir(full_dir_path):
                try:
                    output_json_str = self._read_file(os.path.join(full_dir_path, "output.json"))
                    example = {
                        "passage": self._read_file(os.path.join(full_dir_path, "input_passage.txt")),
                        "output": output_json_str,
                    }
                    examples.append(example)
                except FileNotFoundError as e:
                    print(f"Warning: Skipping directory {example_dir} because a required file is missing: {e}")
        print(f"✅ Loaded {len(examples)} few-shot question examples.")
        return examples

    def _read_file(self, path: str) -> str:
        """파일을 읽어 문자열로 반환하는 유틸리티 함수"""
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Cannot find a file. Path is invalid: {path}")