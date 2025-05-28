from crewai import Task

def create_grammar_correction_task(agent, user_text):
    return Task(
        description=f"""As a friendly English tutor, analyze this text: '{user_text}'
        1. First, engage with the content naturally - what is the person trying to say?
        2. Then, provide the corrected version while maintaining the original meaning
        3. Keep your tone warm and encouraging
        4. If it's a question, acknowledge it before correcting
        5. If it's a statement, show interest in the topic
        Remember to respond conversationally, not just with corrections.""",
        agent=agent,
        expected_output="A natural, conversational response that includes both engagement with the content and corrections."
    )