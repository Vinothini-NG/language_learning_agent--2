from crewai import Task

def create_explanation_task(agent, user_text, corrected_text):
    return Task(
        description=f"""As a supportive tutor, help explain the improvements in this text:
        Original: '{user_text}'
        Corrected: '{corrected_text}'
        
        1. Start with positive reinforcement about what was done well
        2. Explain changes in a friendly, conversational way
        3. Use relatable examples or situations
        4. Add encouraging tips for future practice
        5. Keep the tone supportive and engaging
        
        Make it feel like a friendly chat, not a formal lesson.""",
        agent=agent,
        expected_output="A friendly, encouraging explanation that feels like advice from a supportive friend."
    )