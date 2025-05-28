from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

class VocabularyAgent:
    def __init__(self):
        self.agent = Agent(
            role="Word Coach",
            goal="Suggest simple and better word choices",
            backstory="A friendly guide who helps you find the right words",
            verbose=True,
            llm=ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=os.getenv("GOOGLE_API_KEY")
            )
        )