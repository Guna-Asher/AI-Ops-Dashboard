import json
import google.generativeai as genai
from app.core.config import settings

class AIClient:
    def __init__(self):
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def analyze_incident(self, incident: dict, logs: str) -> str:
        prompt = f"""
        Analyze the following incident and provide root cause and recommendations.
        Incident: {json.dumps(incident)}
        Logs: {logs}
        """
        response = self.model.generate_content(prompt)
        return response.text.strip()