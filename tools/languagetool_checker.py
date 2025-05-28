from langchain.tools import BaseTool
import language_tool_python
import os

# Set the environment variable for LanguageTool JAR directory
os.environ['LTP_JAR_DIR_PATH'] = os.path.join(os.path.dirname(__file__), "..", "languagetool", "LanguageTool-6.4")

class LanguageToolChecker(BaseTool):
    name = "LanguageToolChecker"
    description = "A tool for checking and correcting grammar and spelling errors in text."

    def _run(self, text: str) -> str:
        """Check and correct grammar and spelling errors in the given text."""
        tool = language_tool_python.LanguageTool('en-US')
        matches = tool.check(text)
        corrected = language_tool_python.utils.correct(text, matches)
        return corrected

    def _arun(self, text: str) -> str:
        """Async run method, not implemented as LanguageTool does not support async operations."""
        raise NotImplementedError("LanguageToolChecker does not support async operations.")