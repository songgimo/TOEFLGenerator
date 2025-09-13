
class QuestionThoughtProcessAgent:
    """
    주어진 지문과 질문 JSON을 바탕으로,
    질문 생성 과정의 "사고 과정(Thought Process)"을 생성하는 헬퍼 에이전트입니다.
    """

    def __init__(self):
        print("Initializing Question Thought Process Agent")
        self.llm_client = GoogleLLMClient(
            model_name=GeminiModel.GEMINI_2_5_FLASH,
            temperature=0.5  # 약간 더 결정론적인 결과물을 위해 온도를 낮춥니다.
        )
        self.prompt_template = self._load_prompt_template()
        print("✅ Question Thought Process Agent initialized.")

    def _load_prompt_template(self) -> PromptTemplate:
        """사고 과정 생성을 위한 프롬프트 템플릿을 로드합니다."""
        try:
            with open("prompts/reading/question_thought_process_instruction.txt", "r", encoding="utf-8") as f:
                prompt_text = f.read()

            return PromptTemplate(
                template=prompt_text,
                input_variables=["passage", "json_output"],
            )
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Instruction file not found: {e}")

    def generate_thought_process(self, passage: str, json_output: str) -> str:
        """
        사고 과정 텍스트를 생성합니다.

        Args:
            passage (str): 원본 TOEFL 지문 텍스트.
            json_output (str): 생성된 질문 세트가 담긴 JSON 형식의 문자열.

        Returns:
            str: LLM이 생성한 사고 과정 텍스트.
        """
        print("\n▶️ Generating thought process for the question set...")

        # 프롬프트에 실제 데이터 주입
        final_prompt = self.prompt_template.format(
            passage=passage,
            json_output=json_output
        )

        # LLM 호출
        thought_process = self.llm_client.invoke(final_prompt)

        print("✅ Thought process generated successfully.")
        return thought_process
