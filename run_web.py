import streamlit as st
from agents.reading_passage import ReadingPassageAgent
from agents.reading_question import ReadingQuestionAgent
# Add new imports
from agents.quality_assurance import QualityAssuranceAgent
from config import BaseQuestionSet, EvaluationResult
from typing import Tuple


@st.cache_resource
def load_agents() -> Tuple[ReadingPassageAgent, ReadingQuestionAgent, QualityAssuranceAgent]:
    print("--- 에이전트 초기화 중 ---")
    passage_agent = ReadingPassageAgent()
    question_agent = ReadingQuestionAgent()
    qa_agent = QualityAssuranceAgent()
    print("--- ✅ 에이전트 초기화 완료 ---")
    return passage_agent, question_agent, qa_agent


def initialize_session_state():
    if 'task_generated' not in st.session_state:
        st.session_state.task_generated = False
        st.session_state.passage = ""
        st.session_state.questions_set = None
        st.session_state.evaluation_result = None


def generate_task_and_update_state(topic: str, passage_agent: ReadingPassageAgent, question_agent: ReadingQuestionAgent,
                                   qa_agent: QualityAssuranceAgent):
    display_topic = topic if topic and topic.strip().lower() != 'random' else "a randomly generated academic topic"

    with st.spinner(f"🔥 '{display_topic}'에 대한 TOEFL Task 생성 및 평가 중..."):
        try:
            passage = passage_agent.run(display_topic)
            questions_set = question_agent.run(passage)

            eval_inputs = {"passage": passage, "questions_set": questions_set}
            evaluation_result = qa_agent.run(eval_inputs)

            st.session_state.passage = passage
            st.session_state.questions_set = questions_set
            st.session_state.evaluation_result = evaluation_result
            st.session_state.task_generated = True
            st.success("🎉 TOEFL Task 생성 및 평가가 완료되었습니다!")
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
            st.session_state.task_generated = False


def display_evaluation_interface(result: EvaluationResult):
    st.divider()
    st.header("🤖 AI Quality Assurance Report")

    summary = result.overall_summary
    if summary.final_decision == "Pass":
        st.success(f"**Final Decision: {summary.final_decision}**")
    else:
        st.error(f"**Final Decision: {summary.final_decision}**")

    st.markdown(f"**Justification:** {summary.justification}")

    with st.expander("Show Detailed Scores"):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Passage Quality")
            for key, value in result.evaluation_scores.passage_quality.model_dump().items():
                st.metric(label=key.replace('_', ' ').title(), value=f"{value['score']}/5")

        with col2:
            st.subheader("Question Set Quality")
            for key, value in result.evaluation_scores.question_set_quality.model_dump().items():
                st.metric(label=key.replace('_', ' ').title(), value=f"{value['score']}/5")


def display_task_interface(passage: str, questions_set: BaseQuestionSet):
    st.divider()
    st.header("📖 Reading Passage")
    st.markdown(passage)

    st.divider()
    st.header("📝 Questions")
    if questions_set:
        for i, q in enumerate(questions_set.questions):
            with st.expander(f"**Question {i + 1}: {q.question_type}**", expanded=False):
                # ... (내부 로직 변경 없음)
                if q.question_type == "Sentence Simplification":
                    st.markdown(f"**Original Sentence:** \"_{q.highlighted_sentence}_\"")
                elif q.question_type == "Insert Text":
                    st.markdown(f"**Sentence to Insert:** \"_{q.sentence_to_insert}_\"")
                st.markdown(q.question)
                options = [opt for opt in q.options]
                user_choice = st.radio("Select your answer:", options, key=f"q_{i}", label_visibility="collapsed")

    st.divider()

    if st.checkbox("Show Answer Key", key="show_answers"):
        # ... (내부 로직 변경 없음)
        st.header("🔑 Answer Key")
        if questions_set:
            for i, q in enumerate(questions_set.questions):
                answer_text = ", ".join(q.answer) if isinstance(q.answer, list) else q.answer
                st.write(f"**Question {i + 1}:** {answer_text}")


def main():
    st.set_page_config(page_title="TOEFL Reading Task Generator", layout="wide")
    st.title("📚 TOEFL Reading Task Generator")

    initialize_session_state()
    passage_agent, question_agent, qa_agent = load_agents()

    topic = st.text_input(
        "Enter an academic topic for the Reading passage (or leave blank for random):",
        key="topic_input"
    )

    if st.button("Generate & Evaluate Task", key="generate_button"):
        generate_task_and_update_state(topic, passage_agent, question_agent, qa_agent)

    if st.session_state.task_generated:
        if st.session_state.evaluation_result:
            display_evaluation_interface(st.session_state.evaluation_result)

        display_task_interface(st.session_state.passage, st.session_state.questions_set)


if __name__ == '__main__':
    main()