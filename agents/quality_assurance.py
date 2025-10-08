from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from agents.base import BaseAgent
from llm_client import GoogleLLMClient
from config import GeminiModel, BaseQuestionSet, EvaluationResult
import json


class QualityAssuranceAgent(BaseAgent[dict, EvaluationResult]):
    """
    An agent that evaluates the quality of a generated TOEFL task
    and returns a structured EvaluationResult.
    """

    def _initialize_agent(self):
        """Initializes the LLM client, parser, and prompt template for evaluation."""
        self.llm_client = GoogleLLMClient(
            model_name=GeminiModel.GEMINI_2_5_FLASH,
            temperature=0.2
        )
        self.parser = PydanticOutputParser(pydantic_object=EvaluationResult)
        with open("prompts/reading/quality_assurance_instruction.txt", "r", encoding="utf-8") as f:
            prompt_text = f.read()

        self.prompt_template = PromptTemplate(
            template=prompt_text,
            input_variables=["passage_text", "questions_json"],
            partial_variables={"json_output": self.parser.get_format_instructions()}
        )

    def run(self, inputs: dict) -> EvaluationResult:
        """
        Takes a passage and question set, evaluates them, and returns the structured result.

        Args:
            inputs (dict): A dictionary containing 'passage' (str) and 'questions_set' (BaseQuestionSet).

        Returns:
            EvaluationResult: A Pydantic object containing the detailed evaluation.
        """
        print("\n▶️ Evaluating generated task quality...")

        passage = inputs.get("passage")
        questions_set = inputs.get("questions_set")

        if not passage or not questions_set:
            raise ValueError("Inputs must contain 'passage' and 'questions_set'.")

        questions_json_str = questions_set.model_dump_json(indent=2)

        final_prompt = self.prompt_template.format(
            passage_text=passage,
            questions_json=questions_json_str
        )

        llm_output = self.llm_client.invoke(final_prompt)
        parsed_result = self.parser.parse(llm_output)

        print(f"✅ Evaluation complete. Final Decision: {parsed_result.overall_summary.final_decision}")
        return parsed_result

if __name__ == '__main__':
    qa_agent = QualityAssuranceAgent()
    with open("prompts/reading/question_examples/example_02/input_passage.txt", "r", encoding="utf-8") as f:
        passage_text = f.read()

    with open("prompts/reading/question_examples/example_02/output.json", "r", encoding="utf-8") as f:
        questions_json_string = f.read()

    try:
        questions_set_object = BaseQuestionSet.model_validate_json(questions_json_string)
    except Exception as e:
        print(f"Error parsing JSON into BaseQuestionSet: {e}")
        exit()

    ips = {
        "passage": passage_text,
        "questions_set": questions_set_object
    }
    qa_agent.run(
        ips
    )