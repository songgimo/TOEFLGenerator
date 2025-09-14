import traceback
import json
from agents.thought_process import QuestionThoughtProcessAgent


def read_file(path: str) -> str:
    """테스트를 위한 간단한 파일 읽기 함수"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Test file not found at {path}")
        return ""


def test_thought_process_agent():
    """
    QuestionThoughtProcessAgent가 정상적으로 사고 과정 텍스트를 생성하는지 테스트합니다.
    """
    print("--- Starting Test for QuestionThoughtProcessAgent ---")

    try:
        # 1. 테스트에 필요한 데이터 로드
        # 기존의 example_01을 "문제지"와 "정답지"로 사용합니다.
        passage_to_analyze = read_file("prompts/reading/question_examples/example_01/input_passage.txt")
        json_to_analyze = read_file("prompts/reading/question_examples/example_01/output.json")

        if not passage_to_analyze or not json_to_analyze:
            raise Exception("Failed to load test data files.")

        # 2. 에이전트 초기화
        agent = QuestionThoughtProcessAgent()

        # 3. 에이전트 실행
        # 입력이 dict 형태이므로, 딕셔너리로 만들어 전달합니다.
        inputs = {
            "passage": passage_to_analyze,
            "json_output": json_to_analyze
        }
        generated_thought_process = agent.run(inputs)

        # 4. 결과 검증
        print("\n✅ Agent executed successfully. Now verifying output...")
        assert isinstance(generated_thought_process, str), "FAIL: Output type should be str."
        assert len(generated_thought_process) > 500, "FAIL: Generated text seems too short."
        assert "Deconstruct the Goal" in generated_thought_process, "FAIL: Key section 'Deconstruct the Goal' is missing."

        print("PASS: Output is a non-empty string and contains expected sections.")

        print("\n--- Test Summary ---")
        print("🎉 All assertions passed! The agent is generating thought processes.")

        # 5. 생성된 사고 과정을 파일로 저장 (가장 중요한 활용 단계)
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