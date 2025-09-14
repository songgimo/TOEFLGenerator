import os
import shutil
import argparse
from agents.thought_process import QuestionThoughtProcessAgent


def read_file(path: str) -> str:
    """간단한 파일 읽기 함수"""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def create_new_question_example(passage_path: str, json_path: str):
    """
    새로운 reading question few-shot 예제를 자동 생성하고 저장합니다.
    """
    print("--- Starting: Create New Few-shot Example ---")

    # 1. 입력 파일들이 존재하는지 확인
    if not os.path.exists(passage_path) or not os.path.exists(json_path):
        print(f"❌ Error: Input file not found. Check paths: {passage_path}, {json_path}")
        return

    # 2. 새로운 예제 폴더 번호 결정
    base_dir = "prompts/reading/question_examples"
    existing_dirs = [d for d in os.listdir(base_dir) if d.startswith("example_")]
    next_example_num = len(existing_dirs) + 1
    new_example_dir = os.path.join(base_dir, f"example_{next_example_num:02d}")
    os.makedirs(new_example_dir, exist_ok=True)
    print(f"📂 Creating new example directory: {new_example_dir}")

    # 3. 입력 파일 로드
    passage_content = read_file(passage_path)
    json_content = read_file(json_path)

    # 4. ThoughtProcessAgent를 사용하여 사고 과정 생성
    try:
        agent = QuestionThoughtProcessAgent()
        inputs = {"passage": passage_content, "json_output": json_content}
        thought_process_content = agent.run(inputs)
    except Exception as e:
        print(f"❌ Error during thought process generation: {e}")
        shutil.rmtree(new_example_dir)  # 실패 시 생성된 폴더 삭제
        return

    # 5. 3개의 파일을 새로운 예제 폴더에 저장
    shutil.copy(passage_path, os.path.join(new_example_dir, "input_passage.txt"))
    shutil.copy(json_path, os.path.join(new_example_dir, "output.json"))
    with open(os.path.join(new_example_dir, "thought_process.txt"), "w", encoding="utf-8") as f:
        f.write(thought_process_content)

    print("\n--- ✅ Success! ---")
    print(f"A new few-shot example has been successfully created at: {new_example_dir}")


if __name__ == '__main__':
    # 명령줄에서 파일 경로를 받을 수 있도록 설정
    parser = argparse.ArgumentParser(description="Create a new few-shot example for Reading Questions.")
    parser.add_argument("passage_file", type=str, help="Path to the input_passage.txt file.")
    parser.add_argument("json_file", type=str, help="Path to the output.json file.")

    args = parser.parse_args()

    create_new_question_example(args.passage_file, args.json_file)