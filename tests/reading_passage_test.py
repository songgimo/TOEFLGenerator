import traceback
from agents.reading_passage import ReadingPassageAgent  # 수정된 임포트 경로

SAMPLE_TOPIC = "Random Topic generate"


def test_reading_passage_agent():
    """
    ReadingPassageAgent의 run 메서드가 정상적으로 작동하는지 테스트합니다.
    """
    print("--- Starting Test for ReadingPassageAgent ---")

    try:
        # 1. 에이전트 초기화
        # 이 과정에서 Few-shot 예제를 로딩합니다.
        agent = ReadingPassageAgent()

        # 2. 에이전트 실행
        # BaseAgent 추상화 덕분에 .run() 메서드를 호출합니다.
        result_passage = agent.run(SAMPLE_TOPIC)

        # 3. 결과 검증 (Assertions)
        print("\n✅ Agent executed successfully. Now verifying output...")

        # 3-1. 반환 타입이 문자열(str)인지 확인
        assert isinstance(result_passage, str), f"FAIL: Output type should be str, but got {type(result_passage)}"
        print("PASS: Output type is correct (str).")

        # 3-2. 생성된 지문이 비어있지 않고, 충분한 길이를 가졌는지 확인
        assert result_passage is not None and len(
            result_passage) > 500, f"FAIL: Passage seems too short or is empty. Length: {len(result_passage)}"
        print(f"PASS: Generated passage has a sufficient length ({len(result_passage)} characters).")

        print("\n--- Test Summary ---")
        print("🎉 All assertions passed! The ReadingPassageAgent is working as expected.")

        # 4. 생성된 내용 일부 출력 (시각적 확인용)
        print("\n--- Snippet of Generated Passage ---")
        print(result_passage[:400] + "...")  # 처음 400자만 출력

    except Exception as e:
        print("\n--- 🚨 TEST FAILED 🚨 ---")
        print(f"An error occurred during the test: {e}")
        traceback.print_exc()


# 이 파일이 직접 실행될 때만 테스트 함수를 호출합니다.
if __name__ == '__main__':
    test_reading_passage_agent()