import streamlit as st
from agents.reading_passage import ReadingPassageAgent
from agents.reading_question import ReadingQuestionAgent


def main():
    """
    Streamlit을 사용하여 TOEFL Reading 문제를 생성하고 표시하는 웹 앱
    """
    st.set_page_config(page_title="TOEFL Reading Task Generator", layout="wide")
    st.title("📚 TOEFL Reading Task Generator")

    # 세션 상태(Session State) 초기화
    if 'task_generated' not in st.session_state:
        st.session_state.task_generated = False
        st.session_state.passage = ""
        st.session_state.questions_set = None

    # 사용자 입력
    topic = st.text_input(
        "Enter an academic topic for the Reading passage (or leave blank for random):",
        key="topic_input"
    )

    # 문제 생성 버튼
    if st.button("Generate Task", key="generate_button"):
        if not topic or topic.strip().lower() == 'random':
            display_topic = "a randomly generated academic topic"
        else:
            display_topic = topic

        with st.spinner(f"🔥 Generating TOEFL Reading Task on '{display_topic}'... Please wait."):
            try:
                # 에이전트 초기화
                passage_agent = ReadingPassageAgent()
                question_agent = ReadingQuestionAgent()

                # 지문 및 문제 생성
                st.session_state.passage = passage_agent.generate_passage(display_topic)
                st.session_state.questions_set = question_agent.generate_questions(st.session_state.passage)
                st.session_state.task_generated = True
                st.success("🎉 TOEFL Reading Task Generation Complete!")
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.session_state.task_generated = False


    # 생성된 결과 표시
    if st.session_state.task_generated:
        st.divider()

        # 지문 표시
        st.header("📖 Reading Passage")
        st.markdown(st.session_state.passage)

        st.divider()

        # 문제 표시
        st.header("📝 Questions")
        if st.session_state.questions_set:
            for i, q in enumerate(st.session_state.questions_set.questions):
                st.subheader(f"Question {i+1} ({q.question_type})")

                # 문제 유형에 따라 다르게 표시
                if q.question_type == "Sentence Simplification":
                    st.markdown(f"**Original Sentence:** \"_{q.highlighted_sentence}_\"")

                if q.question_type == "Insert Text":
                     st.markdown(f"**Sentence to Insert:** \"_{q.sentence_to_insert}_\"")

                st.markdown(q.question)

                # 선택지 (Radio button으로 구현)
                options = [opt for opt in q.options]
                user_choice = st.radio(
                    label="Select your answer:",
                    options=options,
                    key=f"q_{i}",
                    label_visibility="collapsed"
                )

        st.divider()

        # 정답 공개
        if st.checkbox("Show Answer Key", key="show_answers"):
            st.header("🔑 Answer Key")
            if st.session_state.questions_set:
                for i, q in enumerate(st.session_state.questions_set.questions):
                    answer_text = ", ".join(q.answer) if isinstance(q.answer, list) else q.answer
                    st.write(f"**Question {i+1}:** {answer_text}")


if __name__ == '__main__':
    main()