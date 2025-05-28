from crewai import Task

def create_vocabulary_task(agent, corrected_text):
    return Task(
        description=f"""As an enthusiastic language partner, suggest vocabulary improvements for: '{corrected_text}'
        
        1. Start with appreciation for the current word choices
        2. Suggest alternatives in a conversational way, like 'You might also say...' or 'Here's a fun word...'
        3. Explain when and why to use each suggestion
        4. Include casual examples in real-life situations
        5. Make it interactive by asking questions about preferences
        
        Focus on making it feel like a natural conversation about words, not a vocabulary lesson.""",
        agent=agent,
        expected_output="Engaging vocabulary suggestions that feel like recommendations from a friend who loves words."
    )