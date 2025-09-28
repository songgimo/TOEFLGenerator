import traceback
from agents.quality_assurance import QualityAssuranceAgent
from config import BaseQuestionSet, EvaluationResult


def test_quality_assurance_agent():
    """
    Tests if the QualityAssuranceAgent runs correctly and produces a structured evaluation.
    """
    print("--- Starting Test for QualityAssuranceAgent ---")

    try:
        # 1. Load the test data (passage and generated questions)
        with open("prompts/reading/question_examples/example_02/input_passage.txt", "r", encoding="utf-8") as f:
            passage_text = f.read()

        with open("prompts/reading/question_examples/example_02/output.json", "r", encoding="utf-8") as f:
            questions_json_string = f.read()

        # 2. Prepare the inputs for the agent
        # The agent expects a Pydantic object, not a JSON string
        questions_set_object = BaseQuestionSet.model_validate_json(questions_json_string)

        inputs = {
            "passage": passage_text,
            "questions_set": questions_set_object
        }

        # 3. Initialize and run the agent
        agent = QualityAssuranceAgent()
        result = agent.run(inputs)

        # 4. Verify the output (Assertions)
        print("\n✅ Agent executed successfully. Now verifying output...")

        # 4-1. Check if the output is the correct Pydantic model instance
        assert isinstance(result,
                          EvaluationResult), f"FAIL: Output type should be EvaluationResult, but got {type(result)}"
        print("PASS: Output type is correct (EvaluationResult).")

        # 4-2. Check for the existence of major attributes
        assert hasattr(result, 'evaluation_scores'), "FAIL: Result is missing 'evaluation_scores' attribute."
        assert hasattr(result, 'overall_summary'), "FAIL: Result is missing 'overall_summary' attribute."
        print("PASS: Result contains the required main attributes.")

        # 4-3. Check for the final decision attribute
        assert result.overall_summary.final_decision in ["Pass",
                                                         "Fail"], f"FAIL: Final decision must be 'Pass' or 'Fail', but got '{result.overall_summary.final_decision}'"
        print(f"PASS: Final decision is valid ('{result.overall_summary.final_decision}').")

        print("\n--- Test Summary ---")
        print("🎉 All assertions passed! The QualityAssuranceAgent is working as expected.")

        # 5. Print a sample of the result for visual inspection
        print("\n--- Generated Evaluation Summary ---")
        print(f"Final Decision: {result.overall_summary.final_decision}")
        print(f"Justification: {result.overall_summary.justification}")
        print("\n--- Detailed Scores ---")
        print(result.evaluation_scores.model_dump_json(indent=2))


    except Exception as e:
        print("\n--- 🚨 TEST FAILED 🚨 ---")
        print(f"An error occurred during the test: {e}")
        traceback.print_exc()


# This allows the test to be run directly from the command line
if __name__ == '__main__':
    test_quality_assurance_agent()






