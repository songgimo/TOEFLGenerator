import os
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from .base import BaseAgent  # BaseAgent 임포트
from llm_client import GoogleLLMClient
from config import GeminiModel


class ReadingPassageAgent(BaseAgent[str, str]):
    """
    주어진 토픽(str)에 대한 TOEFL 읽기 지문(str)을 생성하는 에이전트입니다.
    """

    def _initialize_agent(self):
        """프롬프트 템플릿과 LLM 클라이언트를 초기화합니다."""
        self.llm_client = GoogleLLMClient(
            model_name=GeminiModel.GEMINI_2_5_FLASH,
            temperature=0.7
        )
        self.prompt_template = self._create_few_shot_prompt()

    def run(self, topic: str) -> str:
        """
        토픽을 입력받아 지문을 생성합니다.

        Args:
            topic (str): 생성할 지문의 주제.

        Returns:
            str: 생성된 TOEFL 지문.
        """
        print(f"\n▶️ Generating passage for topic: '{topic}'...")
        final_prompt = self.prompt_template.format(topic=topic)
        passage = self.llm_client.invoke(final_prompt)
        print("✅ Passage generated successfully.")
        return passage

    def _create_few_shot_prompt(self) -> FewShotPromptTemplate:
        examples = self._load_examples("prompts/reading/passage_examples")

        example_prompt = PromptTemplate(
            template="Topic:\n{topic}\n\nThought Process:\n{thought_process}\n\nFinal Passage:\n{output}",
            input_variables=["topic", "thought_process", "output"],
        )

        prefix = self._read_file("prompts/reading/passage_instruction.txt")

        # 4. 전체 프롬프트의 끝 부분 (접미사) - 실제 사용자 입력 부분
        suffix = "Topic:\n{topic}\n\nThought Process:"

        # 5. 모든 요소를 조합하여 최종 프롬프트 템플릿 생성
        return FewShotPromptTemplate(
            examples=examples,
            example_prompt=example_prompt,
            prefix=prefix,
            suffix=suffix,
            input_variables=["topic"],
            example_separator="\n\n---\n\n"
        )

    def _load_examples(self, examples_path: str) -> list[dict]:
        examples = []
        for example_dir in sorted(os.listdir(examples_path)):
            full_dir_path = os.path.join(examples_path, example_dir)

            if os.path.isdir(full_dir_path):
                try:
                    example = {
                        "topic": self._read_file(os.path.join(full_dir_path, "topic.txt")),
                        "thought_process": self._read_file(os.path.join(full_dir_path, "thought_process.txt")),
                        "output_passage": self._read_file(os.path.join(full_dir_path, "output_passage.txt")),
                    }
                    examples.append(example)
                except FileNotFoundError as e:
                    print(f"Warning: Skipping directory {example_dir} because a required file is missing: {e}")

        print(f"✅ Loaded {len(examples)} few-shot passage_examples.")
        return examples

    def _read_file(self, path: str) -> str:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Cannot find a prompt file. Path is invalid: {path}")
