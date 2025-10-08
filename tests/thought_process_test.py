import traceback
from agents.thought_process import QuestionThoughtProcessAgent


def read_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Test file not found at {path}")
        return ""


def test_thought_process_agent():
    print("--- Starting Test for QuestionThoughtProcessAgent ---")

    try:
        passage_to_analyze = read_file("prompts/reading/question_examples/example_01/input_passage.txt")
        json_to_analyze = read_file("prompts/reading/question_examples/example_01/output.json")

        if not passage_to_analyze or not json_to_analyze:
            raise Exception("Failed to load test data files.")

        agent = QuestionThoughtProcessAgent()

        inputs = {
            "passage": passage_to_analyze,
            "json_output": json_to_analyze
        }
        generated_thought_process = agent.run(inputs)

        print("\n✅ Agent executed successfully. Now verifying output...")
        assert isinstance(generated_thought_process, str), "FAIL: Output type should be str."
        assert len(generated_thought_process) > 500, "FAIL: Generated text seems too short."
        assert "Deconstruct the Goal" in generated_thought_process, "FAIL: Key section 'Deconstruct the Goal' is missing."

        print("PASS: Output is a non-empty string and contains expected sections.")

        print("\n--- Test Summary ---")
        print("🎉 All assertions passed! The agent is generating thought processes.")

        output_path = "generated_thought_process.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(generated_thought_process)

        print(f"\n✅ Generated thought process has been saved to '{output_path}'.")
        print("   Please open the file to manually review the quality of the generated text.")

    except Exception as e:
        print("\n--- 🚨 TEST FAILED 🚨 ---")
        print(f"An error occurred during the test: {e}")
        traceback.print_exc()


if __name__ == '__main__':
    test_thought_process_agent()