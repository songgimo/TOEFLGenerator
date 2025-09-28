import traceback
from agents.reading_passage import ReadingPassageAgent
from agents.reading_question import ReadingQuestionAgent
# Add new imports
from agents.quality_assurance import QualityAssuranceAgent
from config import BaseQuestionSet, EvaluationResult


def get_user_topic() -> str:
    """사용자로부터 읽기 지문의 주제를 입력받습니다."""
    topic = input("Enter an academic topic for the Reading passage (or 'random'): ")
    return topic if topic and topic.lower() != 'random' else "a randomly generated academic topic"


def generate_task(passage_agent: ReadingPassageAgent, question_agent: ReadingQuestionAgent, topic: str) -> tuple[
    str, BaseQuestionSet]:
    """주어진 주제에 대해 TOEFL Reading 지문과 질문을 생성합니다."""
    print(f"\n🔥 '{topic}' 주제로 TOEFL Reading Task 생성을 시작합니다...")
    generated_passage = passage_agent.run(topic)
    generated_questions_set = question_agent.run(generated_passage)
    print("\n\n🎉 TOEFL Reading Task 생성이 완료되었습니다! 🎉")
    return generated_passage, generated_questions_set


def display_results(passage: str, questions_set: BaseQuestionSet):
    """생성된 지문, 질문 및 정답을 콘솔에 출력합니다."""
    # ... (기존 display_results 함수 내용은 변경 없음)
    print("=" * 50)
    print("\n📖 Reading Passage\n")
    print(passage)
    print("=" * 50)

    print("\n📝 Questions\n")
    for q in questions_set.questions:
        print(f"Q: {q.question} ({q.question_type})")
        for i, opt in enumerate(q.options):
            print(f"  ({chr(65 + i)}) {opt}")
        print("-" * 20)

    input("\nPress Enter to reveal the answer key...")
    print("\n🔑 Answer Key\n")
    for i, q in enumerate(questions_set.questions):
        answer_text = ", ".join(q.answer) if isinstance(q.answer, list) else q.answer
        print(f"{i + 1}. ({q.question_type}) Correct Answer: {answer_text}")


def display_evaluation_results(result: EvaluationResult):
    """품질 평가 결과를 콘솔에 보기 좋게 출력합니다."""
    print("\n" + "=" * 50)
    print("🤖 AI Quality Assurance Report")
    print("=" * 50)

    summary = result.overall_summary
    decision_color = "\033[92m" if summary.final_decision == "Pass" else "\033[91m"
    print(f"\nFinal Decision: {decision_color}{summary.final_decision}\033[0m")
    print(f"Justification: {summary.justification}\n")

    print("--- Detailed Scores (out of 5) ---")
    print("\n[Passage Quality]")
    for key, value in result.evaluation_scores.passage_quality.model_dump().items():
        print(f"- {key.replace('_', ' ').title()}: {value['score']}/5")

    print("\n[Question Set Quality]")
    for key, value in result.evaluation_scores.question_set_quality.model_dump().items():
        print(f"- {key.replace('_', ' ').title()}: {value['score']}/5")
    print("=" * 50)


def run_reading_task():
    """TOEFL Reading 문제 생성 및 평가 전체 과정을 처리합니다."""
    try:
        passage_agent = ReadingPassageAgent()
        question_agent = ReadingQuestionAgent()
        qa_agent = QualityAssuranceAgent()  # QA 에이전트 초기화

        topic = get_user_topic()
        passage, questions_set = generate_task(passage_agent, question_agent, topic)

        # 생성된 결과로 품질 평가 실행
        evaluation_input = {"passage": passage, "questions_set": questions_set}
        evaluation_result = qa_agent.run(evaluation_input)

        display_results(passage, questions_set)
        display_evaluation_results(evaluation_result)  # 평가 결과 출력

    except Exception as ex:
        print(f"\n🚨 Reading task 중 오류가 발생했습니다: {ex}")
        traceback.print_exc()


def main():
    """TOEFL 문제 생성 CLI를 실행하는 메인 함수"""
    # ... (기존 main 함수 내용은 변경 없음)
    while True:
        print("\n" + "=" * 50)
        print("📚 Welcome to the TOEFL Task Generator 😈")
        print("=" * 50)
        task_type = input("Choose a task to generate ('reading' or 'listening', 'exit' to quit): ").lower()

        if task_type == 'reading':
            run_reading_task()
        elif task_type == 'exit':
            print("프로그램을 종료합니다.")
            break
        else:
            print("Invalid choice. Please enter 'reading', 'listening', or 'exit'.")


if __name__ == '__main__':
    main()