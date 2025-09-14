import traceback
from agents.reading_question import ReadingQuestionAgent
from config import BaseQuestionSet

SAMPLE_PASSAGE = """
Social Change and Revolution: Unpacking the Dynamics of Historical Transformation

The trajectory of human civilization is not a smooth, linear progression but a complex tapestry woven with threads of gradual evolution and abrupt, transformative shifts. At the heart of this dynamic lies the phenomenon of social change, an inherent and pervasive aspect of collective human experience. While social change encompasses any alteration in the social structure or cultural patterns of a society over time, revolutions represent a more specific, often dramatic, and profoundly impactful subset: periods of rapid, fundamental, and frequently violent reordering of the political, economic, and social landscape. Understanding the drivers, mechanisms, and consequences of these profound shifts is crucial for any comprehensive analysis of history.

Social change is actuated by a diverse array of interconnected factors, making its study an intricate endeavor. Economic shifts, for instance, have historically served as powerful catalysts. The transition from agrarian to industrial economies, commencing in the late 18th century, fundamentally restructured class relations, engendered unprecedented urbanization, and gave rise to new ideologies centered on labor and capital. Similarly, globalization, characterized by the increasing interdependence of world economies, cultures, and populations, continues to reshape national identities and social contracts. Technological innovation acts as another potent accelerant; from the printing press revolutionizing information dissemination and challenging ecclesiastical authority, to the internet democratizing communication and facilitating new forms of political mobilization, technological advancements consistently disrupt established norms and create novel social paradigms. Ideological movements, such as the Enlightenment's emphasis on reason and individual rights or the various nationalist currents of the 19th and 20th centuries, provide the intellectual frameworks that galvanize collective action and challenge existing hegemonies. Demographic pressures, including rapid population growth, mass migration, and shifts in age distribution, can strain resources, alter labor markets, and ignite social tensions. Finally, environmental factors, such as resource scarcity or climate change, increasingly emerge as critical drivers, compelling societies to adapt or face potential collapse.

Revolutions, as distinct manifestations of social change, are characterized by their intensity and the scope of their intended or actual transformation. Unlike gradual reforms, revolutions aim to dismantle and reconstruct the foundational pillars of a society. They are typically marked by a period of profound instability, often accompanied by widespread violence, as competing factions vie for control. Historians often delineate various typologies of revolutions: political revolutions, exemplified by the French Revolution (1789), primarily target the state apparatus and governmental structure; social revolutions, such as the Russian Revolution (1917), seek to reconfigure the entire social hierarchy and redistribute power among classes; and cultural revolutions, like China's Cultural Revolution (1966-1976), endeavor to radically alter prevailing values, beliefs, and artistic expressions. While distinct, these categories frequently overlap, as political upheaval often precipitates social and cultural reorientations.

The genesis of a revolution is rarely monolithic. It typically involves a confluence of long-term structural grievances—such as economic inequality, political disenfranchisement, or social injustices—that fester beneath the surface, alongside more immediate triggers, often a perceived state weakness or a specific act of repression. The revolutionary process itself can often be understood as progressing through identifiable phases: an initial period of widespread discontent and intellectual ferment, followed by a moderate phase where reformers attempt incremental changes, which may then give way to a more radical phase as extremists gain ascendancy, leading to intense conflict and often terror. This radical phase is frequently succeeded by a Thermidorian reaction, a period of conservative retrenchment where order is restored, often at the expense of revolutionary ideals, and a new, albeit altered, status quo is established. The English Civil War, the American Revolution, and the Iranian Revolution all, in their unique ways, illustrate elements of this complex revolutionary arc.

The consequences and legacies of revolutions are invariably far-reaching and frequently paradoxical. In the immediate aftermath, they often result in immense human suffering, economic disruption, and political instability. Yet, over the long term, they can irrevocably alter the course of history, leading to the establishment of new political systems, the redefinition of citizenship, the redistribution of wealth, and the emergence of novel social identities. The Industrial Revolution, while not a political overthrow, profoundly reshaped global demographics, fostered the rise of the modern factory system, and created the conditions for contemporary capitalism and its associated labor movements. The digital revolution of the late 20th and early 21st centuries, driven by advancements in computing and connectivity, continues to reconfigure communication, commerce, and social interaction on a global scale, presenting new challenges and opportunities for societal organization.

In conclusion, social change and revolution are not mere historical footnotes but fundamental forces that continuously reshape human societies. They are complex, multi-faceted phenomena driven by a dynamic interplay of economic, technological, ideological, demographic, and environmental factors. While revolutions, with their inherent volatility and potential for violence, represent the most acute form of social transformation, even gradual changes can accumulate over time to produce equally profound shifts. Examining these processes through a historical lens allows us to discern patterns, understand the agency of individuals and groups within broader structural constraints, and appreciate the enduring human quest for justice, progress, and often, a radically different future. Their study remains an imperative for comprehending the intricate evolution of human civilization.

"""


def test_reading_question_agent():
    """
    ReadingQuestionAgent의 run 메서드가 정상적으로 작동하는지 테스트합니다.
    """
    print("--- Starting Test for ReadingQuestionAgent ---")

    try:
        # 1. 에이전트 초기화
        agent = ReadingQuestionAgent()

        # 2. 에이전트 실행
        # BaseAgent 추상화 덕분에 .run() 메서드를 호출하면 됩니다.
        result = agent.run(SAMPLE_PASSAGE)

        # 3. 결과 검증 (Assertions)
        print("\n✅ Agent executed successfully. Now verifying output...")

        # 3-1. 반환 타입이 BaseQuestionSet 인스턴스인지 확인
        assert isinstance(result,
                          BaseQuestionSet), f"FAIL: Output type should be BaseQuestionSet, but got {type(result)}"
        print("PASS: Output type is correct (BaseQuestionSet).")

        # 3-2. 생성된 질문의 개수가 10개인지 확인
        assert len(result.questions) == 10, f"FAIL: Expected 10 questions, but got {len(result.questions)}"
        print(f"PASS: Correct number of questions generated ({len(result.questions)}/10).")

        # 3-3. 각 질문에 question_type, question, options, answer 필드가 모두 있는지 확인
        for i, q in enumerate(result.questions):
            assert hasattr(q, 'question_type'), f"FAIL: Question {i} is missing 'question_type'"
            assert hasattr(q, 'question'), f"FAIL: Question {i} is missing 'question'"
            assert hasattr(q, 'options'), f"FAIL: Question {i} is missing 'options'"
            assert hasattr(q, 'answer'), f"FAIL: Question {i} is missing 'answer'"
        print("PASS: All questions have the required fields.")

        print("\n--- Test Summary ---")
        print("🎉 All assertions passed! The agent is working as expected.")

        # 4. 생성된 내용 일부 출력 (시각적 확인용)
        print("\n--- Sample of Generated Questions ---")
        for i, q in enumerate(result.questions[:2]):  # 처음 2개 질문만 출력
            print(f"\n[Question {i + 1}]")
            print(f"  Type: {q.question_type}")
            print(f"  Question: {q.question}")
            print(f"  Options: {len(q.options)} options available")
            answer_text = ", ".join(q.answer) if isinstance(q.answer, list) else q.answer
            print(f"  Answer: {answer_text}")

    except Exception as e:
        print("\n--- 🚨 TEST FAILED 🚨 ---")
        print(f"An error occurred during the test: {e}")
        traceback.print_exc()


# 이 파일이 직접 실행될 때만 테스트 함수를 호출합니다.
if __name__ == '__main__':
    test_reading_question_agent()