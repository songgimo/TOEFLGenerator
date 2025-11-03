from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from .base import BaseAgent
from llm_client import GoogleLLMClient
from config import GeminiModel
from typing import Dict


class ListeningPassageAgent(BaseAgent[str, str]):

    SCENARIOS = ["lecture", "conversation"]
    def _initialize_agent(self):
        self.llm_client = GoogleLLMClient(
            model_name=GeminiModel.GEMINI_2_5_FLASH,
            temperature=0.8
        )

        for scenario in self.SCENARIOS:
            try:
                # _create_few_shot_prompt를 호출하여 템플릿 생성
                self.prompt_templates[scenario] = self._create_few_shot_prompt(scenario)
                print(f"✅ Loaded template for '{scenario}'")
            except FileNotFoundError as e:
                print(f"⚠️ Warning: Could not load prompt template for scenario '{scenario}'. Error: {e}")

        self.prompt_templates: Dict[str, FewShotPromptTemplate] = {}
    def run(self, inputs: Dict[str, str]) -> str:
        scenario = inputs.get("scenario")
        topic = inputs.get("topic")
        if not scenario or not topic:
            raise ValueError("Inputs dictionary must contain 'scenario' and 'topic' keys.")

        print(f"\n▶️ Generating listening script (Scenario: {scenario}, Topic: {topic})...")
        if scenario not in self.prompt_templates:
            raise ValueError(
                f"Invalid or unloaded scenario: '{scenario}'. "
                f"Available loaded scenarios: {list(self.prompt_templates.keys())}"
            )
        prompt_template = self.prompt_templates[scenario]
        final_prompt = prompt_template.format(topic=topic)
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

