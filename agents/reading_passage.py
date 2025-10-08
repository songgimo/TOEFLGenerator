from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from .base import BaseAgent
from llm_client import GoogleLLMClient
from config import GeminiModel


class ReadingPassageAgent(BaseAgent[str, str]):
    def _initialize_agent(self):
        self.llm_client = GoogleLLMClient(
            model_name=GeminiModel.GEMINI_2_5_FLASH, temperature=0.7
        )
        self.prompt_template = self._create_few_shot_prompt()

    def run(self, topic: str) -> str:
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

        suffix = "Topic:\n{topic}\n\nThought Process:"

        return FewShotPromptTemplate(
            examples=examples,
            example_prompt=example_prompt,
            prefix=prefix,
            suffix=suffix,
            input_variables=["topic"],
            example_separator="\n\n---\n\n",
        )
