import traceback
from agents.quality_assurance import QualityAssuranceAgent
from config import BaseQuestionSet, EvaluationResult


def test_quality_assurance_agent():
    print("--- Starting Test for QualityAssuranceAgent ---")

    try:
        with open("prompts/reading/question_examples/example_02/input_passage.txt", "r", encoding="utf-8") as f:
            passage_text = f.read()

        with open("prompts/reading/question_examples/example_02/output.json", "r", encoding="utf-8") as f:
            questions_json_string = f.read()

        questions_set_object = BaseQuestionSet.model_validate_json(questions_json_string)

        inputs = {
            "passage": passage_text,
            "questions_set": questions_set_object
        }

        agent = QualityAssuranceAgent()
        result = agent.run(inputs)

        print("\n✅ Agent executed successfully. Now verifying output...")

        assert isinstance(result,
                          EvaluationResult), f"FAIL: Output type should be EvaluationResult, but got {type(result)}"
        print("PASS: Output type is correct (EvaluationResult).")

        assert hasattr(result, 'evaluation_scores'), "FAIL: Result is missing 'evaluation_scores' attribute."
        assert hasattr(result, 'overall_summary'), "FAIL: Result is missing 'overall_summary' attribute."
        print("PASS: Result contains the required main attributes.")

        assert result.overall_summary.final_decision in ["Pass",
                                                         "Fail"], f"FAIL: Final decision must be 'Pass' or 'Fail', but got '{result.overall_summary.final_decision}'"
        print(f"PASS: Final decision is valid ('{result.overall_summary.final_decision}').")

        print("\n--- Test Summary ---")
        print("🎉 All assertions passed! The QualityAssuranceAgent is working as expected.")

        print("\n--- Generated Evaluation Summary ---")
        print(f"Final Decision: {result.overall_summary.final_decision}")
        print(f"Justification: {result.overall_summary.justification}")
        print("\n--- Detailed Scores ---")
        print(result.evaluation_scores.model_dump_json(indent=2))


    except Exception as e:
        print("\n--- 🚨 TEST FAILED 🚨 ---")
        print(f"An error occurred during the test: {e}")
        traceback.print_exc()


if __name__ == '__main__':
    test_quality_assurance_agent()






