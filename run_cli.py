import traceback
from agents.reading_passage import ReadingPassageAgent
from agents.reading_question import ReadingQuestionAgent
from config import BaseQuestionSet

def get_user_topic() -> str:
    """
    사용자로부터 읽기 지문의 주제를 입력받습니다.
    입력이 없거나 'random'일 경우 기본값으로 "a randomly generated academic topic"을 반환합니다.
    """
    topic = input("Enter an academic topic for the Reading passage (or 'random'): ")
    return topic if topic and topic.lower() != 'random' else "a randomly generated academic topic"

def generate_task(passage_agent: ReadingPassageAgent, question_agent: ReadingQuestionAgent, topic: str) -> tuple[str, BaseQuestionSet]:
    """
    주어진 주제에 대해 TOEFL Reading 지문과 질문을 생성합니다.
    """
    print(f"\n🔥 '{topic}' 주제로 TOEFL Reading Task 생성을 시작합니다...")
    generated_passage = passage_agent.run(topic)
    generated_questions_set = question_agent.run(generated_passage)
    print("\n\n🎉 TOEFL Reading Task 생성이 완료되었습니다! 🎉")
    return generated_passage, generated_questions_set

def display_results(passage: str, questions_set: BaseQuestionSet):
    """
    생성된 지문, 질문 및 정답을 콘솔에 출력합니다.
    """
    print("="*50)
    print("\n📖 Reading Passage\n")
    print(passage)
    print("="*50)

    print("\n📝 Questions\n")
    for q in questions_set.questions:
        print(f"Q: {q.question} ({q.question_type})")
        for i, opt in enumerate(q.options):
            print(f"  ({chr(65+i)}) {opt}")
        print("-" * 20)

    input("\nPress Enter to reveal the answer key...")
    print("\n🔑 Answer Key\n")
    for i, q in enumerate(questions_set.questions):
        answer_text = ", ".join(q.answer) if isinstance(q.answer, list) else q.answer
        print(f"{i+1}. ({q.question_type}) Correct Answer: {answer_text}")

def run_reading_task():
    """
    TOEFL Reading 문제 생성 전체 과정을 처리합니다.
    """
    try:
        passage_agent = ReadingPassageAgent()
        question_agent = ReadingQuestionAgent()

        topic = get_user_topic()
        passage, questions_set = generate_task(passage_agent, question_agent, topic)
        display_results(passage, questions_set)

    except Exception as ex:
        print(f"\n🚨 Reading task 중 오류가 발생했습니다: {ex}")
        traceback.print_exc()

def main():
    """
    TOEFL 문제 생성 CLI를 실행하는 메인 함수
    """
    while True:
        print("\n" + "="*50)
        print("📚 Welcome to the TOEFL Task Generator 😈")
        print("="*50)
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