from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

class ExplanationAgent:
    def __init__(self):
        self.agent = Agent(
            role="Grammar Teacher",
            goal="Explain grammar fixes simply and clearly",
            backstory="A friendly teacher who helps you understand grammar mistakes",
            verbose=True,
            llm=ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=os.getenv("GOOGLE_API_KEY")
            )
        )