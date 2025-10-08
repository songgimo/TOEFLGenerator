import traceback
from agents.reading_passage import ReadingPassageAgent

SAMPLE_TOPIC = "Random Topic generate"


def test_reading_passage_agent():
    print("--- Starting Test for ReadingPassageAgent ---")

    try:
        agent = ReadingPassageAgent()

        result_passage = agent.run(SAMPLE_TOPIC)

        print("\n✅ Agent executed successfully. Now verifying output...")

        assert isinstance(result_passage, str), f"FAIL: Output type should be str, but got {type(result_passage)}"
        print("PASS: Output type is correct (str).")

        assert result_passage is not None and len(
            result_passage) > 500, f"FAIL: Passage seems too short or is empty. Length: {len(result_passage)}"
        print(f"PASS: Generated passage has a sufficient length ({len(result_passage)} characters).")

        print("\n--- Test Summary ---")
        print("🎉 All assertions passed! The ReadingPassageAgent is working as expected.")

        print("\n--- Snippet of Generated Passage ---")
        print(result_passage[:400] + "...")

    except Exception as e:
        print("\n--- 🚨 TEST FAILED 🚨 ---")
        print(f"An error occurred during the test: {e}")
        traceback.print_exc()


if __name__ == '__main__':
    test_reading_passage_agent()