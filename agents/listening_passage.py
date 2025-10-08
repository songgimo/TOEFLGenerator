from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from .base import BaseAgent
from llm_client import GoogleLLMClient
from config import GeminiModel


class ListeningPassageAgent(BaseAgent[str, str]):
    def _initialize_agent(self):
        self.llm_client = GoogleLLMClient(
            model_name=GeminiModel.GEMINI_2_5_FLASH,
            temperature=0.8
        )

    def run(self, scenario: str) -> str:
        print(f"\n▶️ Generating listening script (Scenario: {scenario})...")

        prompt_template = self._create_few_shot_prompt(scenario)

        final_prompt = prompt_template.format(scenario=scenario)
        script = self.llm_client.invoke(final_prompt)
        print("✅ Script generated successfully.")
        return script

    def _create_few_shot_prompt(self, scenario: str) -> FewShotPromptTemplate:
        examples_path = f"prompts/listening/{scenario}/passage_examples"
        instruction_path = f"prompts/listening/{scenario}/passage_instruction.txt"

        examples = self._load_examples(examples_path)

        example_prompt = PromptTemplate(
            template="Topic:\n{topic}\n\nThought Process:\n{thought_process}\n\nFinal Script:\n{output}",
            input_variables=["topic", "thought_process", "output"],
        )

        prefix = self._read_file(instruction_path)

        suffix = "Topic:\n{topic}\n\nThought Process:"

        return FewShotPromptTemplate(
            examples=examples,
            example_prompt=example_prompt,
            prefix=prefix,
            suffix=suffix,
            input_variables=["topic"],
            example_separator="\n\n---\n\n",
        )

