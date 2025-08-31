from enum import Enum
from typing import List, Literal, Union
from pydantic import BaseModel, Field


class GeminiModel(Enum):
    """
        An enumeration for Google Gemini model names
    """

    GEMINI_2_5_FLASH = "gemini-2.5-flash"
    GEMINI_2_5_PRO = "gemini-2.5-pro"

    def __str__(self):
        return self.value


class BaseQuestion(BaseModel):
    """모든 질문 모델이 상속받는 기본 클래스입니다."""
    question_type: str = Field(description="The type of question (e.g., 'Main Idea', 'Vocabulary', 'Inference')")
    question: str = Field(description="The question about the given passage_examples")
    options: List[str] = Field(description="A list of 4 multiple-choice options")
    answer: str = Field(description="The text of the correct answer from the 4 options")

class StandardQuestion(BaseQuestion):
    """하나의 질문, 4개의 선택지, 하나의 정답을 갖는 표준 질문 모델입니다."""
    # 'question_type'을 특정 값들로 제한하여 데이터의 정확성을 보장합니다.
    question_type: Literal[
        "Factual Information",
        "Negative Factual Information",
        "Inference",
        "Rhetorical Purpose",
        "Vocabulary-in-Context"
    ]
    question: str = Field(description="The full text of the question.")
    options: List[str] = Field(description="A list of 4 multiple-choice options.", min_items=4, max_items=4)
    answer: str = Field(description="The single correct answer text from the options.")

# 3. 'Sentence Simplification' 전용 모델
class SentenceSimplificationQuestion(BaseQuestion):
    question_type: Literal["Sentence Simplification"]
    highlighted_sentence: str = Field(description="The original sentence from the passage_examples to be simplified.")
    question: str = Field(
        default="Which of the sentences below best expresses the essential information in the highlighted sentence?",
        description="The fixed instruction for this question type."
    )
    options: List[str] = Field(description="A list of 4 sentences as options.", min_items=4, max_items=4)
    answer: str = Field(description="The text of the correct simplified sentence.")

# 4. 'Insert Text' 전용 모델
class InsertTextQuestion(BaseQuestion):
    question_type: Literal["Insert Text"]
    sentence_to_insert: str = Field(description="The sentence that needs to be placed in the passage_examples.")
    question: str = Field(description="The paragraph text containing four squares [1], [2], [3], [4] for insertion.")
    options: List[str] = Field(default=["1", "2", "3", "4"], description="The labels for the insertion points.")
    answer: str = Field(description="The correct label for the insertion point (e.g., '3').")

# 5. 'Prose Summary' 전용 모델
class ProseSummaryQuestion(BaseQuestion):
    question_type: Literal["Prose Summary"]
    introductory_sentence: str = Field(description="The introductory sentence for the summary provided to the user.")
    question: str = Field(
        default="Complete the summary by selecting the THREE answer choices that express the most important ideas.",
        description="The fixed instruction for this question type."
    )
    # 선택지와 정답의 개수를 강제하여 안정성을 높입니다.
    options: List[str] = Field(description="A list of 6 options for the summary.", min_items=6, max_items=6)
    answer: List[str] = Field(description="A list containing the 3 correct answer texts.", min_items=3, max_items=3)


AnyQuestion = Union[
    StandardQuestion,
    SentenceSimplificationQuestion,
    InsertTextQuestion,
    ProseSummaryQuestion,
]
class BaseQuestionSet(BaseModel):
    questions: List[AnyQuestion] = Field(
        discriminator="question_type"
    )
