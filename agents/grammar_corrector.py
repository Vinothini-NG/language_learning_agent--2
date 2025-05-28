from crewai import Agent
from tools.languagetool_checker import LanguageToolChecker
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

class GrammarCorrectorAgent:
    def __init__(self):
        self.agent = Agent(
            role="Grammar Corrector",
            goal="Correct grammar and spelling errors in user-provided text",
            backstory="You are a skilled editor with expertise in English grammar and spelling.",
            verbose=True,
            tools=[LanguageToolChecker()],
            llm=ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=os.getenv("GOOGLE_API_KEY")
            )
        )