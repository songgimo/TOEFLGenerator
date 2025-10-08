import os
import shutil
import argparse
from agents.thought_process import QuestionThoughtProcessAgent


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def create_new_question_example(passage_path: str, json_path: str):
    print("--- Starting: Create New Few-shot Example ---")

    if not os.path.exists(passage_path) or not os.path.exists(json_path):
        print(f"❌ Error: Input file not found. Check paths: {passage_path}, {json_path}")
        return

    base_dir = "prompts/reading/question_examples"
    existing_dirs = [d for d in os.listdir(base_dir) if d.startswith("example_")]
    next_example_num = len(existing_dirs) + 1
    new_example_dir = os.path.join(base_dir, f"example_{next_example_num:02d}")
    os.makedirs(new_example_dir, exist_ok=True)
    print(f"📂 Creating new example directory: {new_example_dir}")

    passage_content = read_file(passage_path)
    json_content = read_file(json_path)

    try:
        agent = QuestionThoughtProcessAgent()
        inputs = {"passage": passage_content, "json_output": json_content}
        thought_process_content = agent.run(inputs)
    except Exception as e:
        print(f"❌ Error during thought process generation: {e}")
        shutil.rmtree(new_example_dir)
        return

    shutil.copy(passage_path, os.path.join(new_example_dir, "input_passage.txt"))
    shutil.copy(json_path, os.path.join(new_example_dir, "output.json"))
    with open(os.path.join(new_example_dir, "thought_process.txt"), "w", encoding="utf-8") as f:
        f.write(thought_process_content)

    print("\n--- ✅ Success! ---")
    print(f"A new few-shot example has been successfully created at: {new_example_dir}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create a new few-shot example for Reading Questions.")
    parser.add_argument("passage_file", type=str, help="Path to the input_passage.txt file.")
    parser.add_argument("json_file", type=str, help="Path to the output.json file.")

    args = parser.parse_args()

    create_new_question_example(args.passage_file, args.json_file)