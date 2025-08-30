# main.py에서 우리가 정의한 에이전트 클래스들을 가져옵니다.
from main import ReadingPassageAgent, ReadingQuestionAgent
import traceback

def run_reading_task():
    """Handles the TOEFL Reading task generation flow."""
    try:
        passage_agent = ReadingPassageAgent()
        question_agent = ReadingQuestionAgent()

        topic = input("Enter an academic topic for the Reading passage_examples (or 'random'): ")
        if not topic or topic.lower() == 'random':
            topic = "a randomly generated academic topic"

        print("\n🔥 Starting TOEFL Reading Task Generation...")
        generated_passage = passage_agent.generate_passage(topic)
        # JSON 출력을 위해 question_instruction.txt 대신 question_json_output.txt를 사용하도록 수정했습니다.
        generated_questions_set = question_agent.generate_questions(generated_passage)


        print("\n\n🎉 TOEFL Reading Task Generation Complete! 🎉")
        print("="*50)
        print("\n📖 Reading Passage\n")
        print(generated_passage)
        print("="*50)

        print("\n📝 Questions\n")
        for q in generated_questions_set.questions:
            print(f"Q: {q.question} ({q.question_type})")
            # Prose Summary는 options가 6개, 나머지는 4개입니다.
            # 모든 옵션을 출력하도록 수정합니다.
            for i, opt in enumerate(q.options):
                print(f"  ({chr(65+i)}) {opt}")
            print("-" * 20)

        input("\nPress Enter to reveal the answer key...")
        print("\n🔑 Answer Key\n")
        for i, q in enumerate(generated_questions_set.questions):
            answer_text = ", ".join(q.answer) if isinstance(q.answer, list) else q.answer
            print(f"{i+1}. ({q.question_type}) Correct Answer: {answer_text}")

    except Exception as ex:
        print(f"An error occurred during the Reading task: {ex}")
        traceback.print_exc()



def main():
    """
    TOEFL 문제 생성 CLI를 실행하는 메인 함수
    """
    while True:
        print("\n" + "="*50)
        print("📚 Welcome to the TOEFL Task Generator 😈")
        print("="*50)
        task_type = input("Choose a task to generate ('reading' or 'listening'): ").lower()

        if task_type == 'reading':
            run_reading_task()
            break
        else:
            print("Invalid choice. Please enter 'reading' or 'listening'.")

# 이 파일이 직접 실행될 때만 main() 함수를 호출합니다.
if __name__ == '__main__':
    main()