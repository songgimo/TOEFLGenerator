from enum import Enum
from typing import List, Literal, Union, Annotated
from pydantic import BaseModel, Field


class GeminiModel(Enum):
    GEMINI_2_5_FLASH = "gemini-2.5-flash"
    GEMINI_2_5_PRO = "gemini-2.5-pro"

    def __str__(self):
        return self.value


class BaseQuestion(BaseModel):
    question_type: str = Field(
        description="The type of question (e.g., 'Main Idea', 'Vocabulary', 'Inference')"
    )
    question: str = Field(description="The question about the given passage_examples")
    options: List[str] = Field(description="A list of 4 multiple-choice options")
    answer: str = Field(description="The text of the correct answer from the 4 options")


class StandardQuestion(BaseQuestion):
    question_type: Literal[
        "Factual Information",
        "Negative Factual Information",
        "Inference",
        "Rhetorical Purpose",
        "Vocabulary-in-Context",
    ]
    question: str = Field(description="The full text of the question.")
    options: List[str] = Field(
        description="A list of 4 multiple-choice options.", min_items=4, max_items=4
    )
    answer: str = Field(description="The single correct answer text from the options.")


class SentenceSimplificationQuestion(BaseQuestion):
    question_type: Literal["Sentence Simplification"]
    highlighted_sentence: str = Field(
        description="The original sentence from the passage_examples to be simplified."
    )
    question: str = Field(
        default="Which of the sentences below best expresses the essential information in the highlighted sentence?",
        description="The fixed instruction for this question type.",
    )
    options: List[str] = Field(
        description="A list of 4 sentences as options.", min_items=4, max_items=4
    )
    answer: str = Field(description="The text of the correct simplified sentence.")


class InsertTextQuestion(BaseQuestion):
    question_type: Literal["Insert Text"]
    sentence_to_insert: str = Field(
        description="The sentence that needs to be placed in the passage_examples."
    )
    question: str = Field(
        description="The paragraph text containing four squares [1], [2], [3], [4] for insertion."
    )
    options: List[str] = Field(
        default=["1", "2", "3", "4"], description="The labels for the insertion points."
    )
    answer: str = Field(
        description="The correct label for the insertion point (e.g., '3')."
    )


class ProseSummaryQuestion(BaseQuestion):
    question_type: Literal["Prose Summary"]
    introductory_sentence: str = Field(
        description="The introductory sentence for the summary provided to the user."
    )
    question: str = Field(
        default="Complete the summary by selecting the THREE answer choices that express the most important ideas.",
        description="The fixed instruction for this question type.",
    )
    # 선택지와 정답의 개수를 강제하여 안정성을 높입니다.
    options: List[str] = Field(
        description="A list of 6 options for the summary.", min_items=6, max_items=6
    )
    answer: List[str] = Field(
        description="A list containing the 3 correct answer texts.",
        min_items=3,
        max_items=3,
    )


AnyQuestion = Union[
    StandardQuestion,
    SentenceSimplificationQuestion,
    InsertTextQuestion,
    ProseSummaryQuestion,
]


class BaseQuestionSet(BaseModel):
    questions: List[Annotated[AnyQuestion, Field(discriminator="question_type")]]


class ScoreItem(BaseModel):
    score: int = Field(description="The score from 1 to 5.", ge=1, le=5)
    comment: str = Field(description="A brief comment justifying the score.")


class PassageQualityScores(BaseModel):
    word_count: ScoreItem
    readability: ScoreItem
    vocabulary_distribution: ScoreItem
    academic_logic_and_cohesion: ScoreItem
    tone: ScoreItem


class QuestionSetQualityScores(BaseModel):
    clarity_of_stem: ScoreItem
    unambiguous_correct_answer: ScoreItem
    plausible_distractors: ScoreItem
    passage_dependency: ScoreItem
    question_variety: ScoreItem


class EvaluationScores(BaseModel):
    passage_quality: PassageQualityScores
    question_set_quality: QuestionSetQualityScores


class OverallSummary(BaseModel):
    final_decision: Literal["Pass", "Fail"]
    justification: str = Field(description="A concise summary of the evaluation.")


class EvaluationResult(BaseModel):
    evaluation_scores: EvaluationScores
    overall_summary: OverallSummary
