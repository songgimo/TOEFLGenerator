import os
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser

from .base import BaseAgent
from llm_client import GoogleLLMClient
from config import GeminiModel, BaseQuestionSet


class ReadingQuestionAgent(BaseAgent[str, BaseQuestionSet]):

    def _initialize_agent(self):
        self.llm_client = GoogleLLMClient(
            model_name=GeminiModel.GEMINI_2_5_FLASH,
            temperature=0.7,
        )
        self.parser = PydanticOutputParser(pydantic_object=BaseQuestionSet)
        self.prompt_template = self._create_few_shot_prompt()

    def run(self, passage: str) -> BaseQuestionSet:
        print("\n▶️ Generating questions for the passage...")

        final_prompt = self.prompt_template.format(passage=passage)
        llm_output = self.llm_client.invoke(final_prompt)

        question_set = self.parser.parse(llm_output)

        print("✅ Questions generated successfully.")
        return question_set

    def _create_few_shot_prompt(self) -> FewShotPromptTemplate:
        examples = self._load_examples("prompts/reading/question_examples")

        example_prompt = PromptTemplate(
            template="Passage:\n{{passage}}\n\nJSON Output:\n{{output}}",
            input_variables=["passage", "output"],
            template_format="jinja2",
        )

        prefix = self._read_file("prompts/reading/question_instruction.txt")

        suffix = "Passage:\n{{passage}}\n\nJSON Output:"

        return FewShotPromptTemplate(
            examples=examples,
            example_prompt=example_prompt,
            prefix=prefix,
            suffix=suffix,
            input_variables=["passage"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            },
            template_format="jinja2",
            example_separator="\n\n---\n\n",
        )

    def _load_examples(self, examples_path: str) -> list[dict]:
        examples = []
        for example_dir in sorted(os.listdir(examples_path)):
            full_dir_path = os.path.join(examples_path, example_dir)
            if os.path.isdir(full_dir_path):
                try:
                    output_json_str = self._read_file(
                        os.path.join(full_dir_path, "output.json")
                    )
                    example = {
                        "passage": self._read_file(
                            os.path.join(full_dir_path, "input_passage.txt")
                        ),
                        "output": output_json_str,
                    }
                    examples.append(example)
                except FileNotFoundError as e:
                    print(
                        f"Warning: Skipping directory {example_dir} because a required file is missing: {e}"
                    )
        print(f"✅ Loaded {len(examples)} few-shot question examples.")
        return examples
