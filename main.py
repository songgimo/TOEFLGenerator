import os
import json

from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from config import GeminiModel, BaseQuestionSet
from llm_client import GoogleLLMClient
from typing import Literal


class BaseAgent:
    ...



class ReadingPassageAgent:
    def __init__(self):
        print("Initializing Reading Passage Agent")
        self.llm_client = GoogleLLMClient(
            model_name=GeminiModel.GEMINI_2_5_FLASH,
            temperature=0.7
        )

        self.prompt_template = self._create_few_shot_prompt()
        print("✅ Reading Passage Agent initialized.")

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

    def generate_passage(self, topic: str) -> str:
        """
            Generates a reading passage_examples on a given topic.
            Args:
                topic (str): topic to generate passage_examples for.

            Returns:
                str: text which response from LLM.
        """
        print(f"\n▶️ Generating passage_examples for topic: '{topic}'...")

        final_prompt = self.prompt_template.format(topic=topic)

        passage = self.llm_client.invoke(final_prompt)

        print("✅ Passage generated successfully.")
        return passage


class ReadingQuestionAgent:
    def __init__(self):
        print("Initializing Reading Question Prompt")
        self.llm_client = GoogleLLMClient(
            model_name=GeminiModel.GEMINI_2_5_FLASH,
            temperature=0.7,
        )
        self.parser = JsonOutputParser(pydantic_object=BaseQuestionSet)
        self.prompt_template = self._load_prompt_template_with_parser(
            "prompts/reading/question_instruction.txt", self.parser
        )
        self.chain = self.prompt_template | self.llm_client.llm | self.parser
        print("✅ Reading Question Agent initialized.")


    def _load_prompt_template_with_parser(self, path: str, parser: JsonOutputParser) -> PromptTemplate:
        try:
            with open(path, "r", encoding="utf-8") as f:
                prompt_text = f.read()
            return PromptTemplate(
                template=prompt_text,
                input_variables=["passage_examples"],
                # 파서로부터 받은 JSON 형식 지시사항을 프롬프트에 주입합니다.
                partial_variables={"format_instructions": parser.get_format_instructions()}
            )
        except FileNotFoundError:
            raise FileNotFoundError(f"프롬프트 파일을 찾을 수 없습니다: {path}")

    def generate_questions(self, passage: str) -> BaseQuestionSet:
        """
        Generates a set of questions for a given passage_examples.
        """
        print("\n▶️ Generating questions for the passage_examples...")
        # 체인을 호출하여 구조화된 질문 생성
        question_set = self.chain.invoke({"passage_examples": passage})
        print("✅ Questions generated successfully.")
        return question_set

