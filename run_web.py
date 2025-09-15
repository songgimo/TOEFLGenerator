import streamlit as st
from agents.reading_passage import ReadingPassageAgent
from agents.reading_question import ReadingQuestionAgent
from config import BaseQuestionSet
from typing import Tuple


@st.cache_resource
def load_agents() -> Tuple[ReadingPassageAgent, ReadingQuestionAgent]:
    """
    ReadingPassageAgent와 ReadingQuestionAgent를 초기화하고 캐시합니다.
    Streamlit의 cache_resource를 사용하여 앱 실행 동안 에이전트가 한 번만 로드되도록 합니다.
    """
    print("--- 에이전트 초기화 중 ---")
    passage_agent = ReadingPassageAgent()
    question_agent = ReadingQuestionAgent()
    print("--- ✅ 에이전트 초기화 완료 ---")
    return passage_agent, question_agent


def initialize_session_state():
    """
    Streamlit 세션 상태를 초기화합니다.
    """
    if 'task_generated' not in st.session_state:
        st.session_state.task_generated = False
        st.session_state.passage = ""
        st.session_state.questions_set = None


def generate_task_and_update_state(topic: str, passage_agent: ReadingPassageAgent,
                                   question_agent: ReadingQuestionAgent):
    """
    주어진 토픽으로 TOEFL Reading 지문과 질문을 생성하고 세션 상태를 업데이트합니다.
    """
    display_topic = topic if topic and topic.strip().lower() != 'random' else "a randomly generated academic topic"

    with st.spinner(f"🔥 '{display_topic}'에 대한 TOEFL Reading Task 생성 중... 잠시만 기다려주세요."):
        try:
            passage = passage_agent.run(display_topic)
            questions_set = question_agent.run(passage)

            st.session_state.passage = passage
            st.session_state.questions_set = questions_set
            st.session_state.task_generated = True
            st.success("🎉 TOEFL Reading Task 생성이 완료되었습니다!")
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
            st.session_state.task_generated = False


def display_task_interface(passage: str, questions_set: BaseQuestionSet):
    """
    생성된 지문, 질문 및 정답을 Streamlit 인터페이스에 표시합니다.
    """
    st.divider()
    st.header("📖 Reading Passage")
    st.markdown(passage)

    st.divider()
    st.header("📝 Questions")
    if questions_set:
        for i, q in enumerate(questions_set.questions):
            with st.expander(f"**Question {i + 1}: {q.question_type}**", expanded=False):
                if q.question_type == "Sentence Simplification":
                    st.markdown(f"**Original Sentence:** \"_{q.highlighted_sentence}_\"")
                elif q.question_type == "Insert Text":
                    st.markdown(f"**Sentence to Insert:** \"_{q.sentence_to_insert}_\"")

                st.markdown(q.question)

                # Prose Summary는 여러 개를 선택해야 하므로 multiselect를 사용하고, 나머지는 radio를 사용합니다.
                if q.question_type == "Prose Summary":
                    st.multiselect("Select your answers:", q.options, key=f"q_{i}")
                else:
                    st.radio("Select your answer:", q.options, key=f"q_{i}", label_visibility="collapsed")

    st.divider()

    if st.checkbox("Show Answer Key", key="show_answers"):
        st.header("🔑 Answer Key")
        if questions_set:
            for i, q in enumerate(questions_set.questions):
                answer_text = ", ".join(q.answer) if isinstance(q.answer, list) else q.answer
                st.write(f"**Question {i + 1}:** {answer_text}")


def main():
    """
    Streamlit을 사용하여 TOEFL Reading 문제를 생성하고 표시하는 메인 웹 앱 함수
    """
    st.set_page_config(page_title="TOEFL Reading Task Generator", layout="wide")
    st.title("📚 TOEFL Reading Task Generator")

    # 세션 상태 및 에이전트 초기화
    initialize_session_state()
    passage_agent, question_agent = load_agents()

    # 사용자 입력 UI
    topic = st.text_input(
        "Enter an academic topic for the Reading passage (or leave blank for random):",
        key="topic_input"
    )

    # 문제 생성 버튼
    if st.button("Generate Task", key="generate_button"):
        generate_task_and_update_state(topic, passage_agent, question_agent)

    # 생성된 결과 표시
    if st.session_state.task_generated:
        display_task_interface(st.session_state.passage, st.session_state.questions_set)


if __name__ == '__main__':
    main()