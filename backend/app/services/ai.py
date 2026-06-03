import json
from typing import Dict, Any
import google.generativeai as genai
from app.core.config import settings

class AIService:
    def __init__(self):
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def analyze_incident(self, incident: Dict[str, Any], logs: str) -> str:
        prompt = f"""
        You are an AI ops assistant. Analyze the following incident and provide root cause analysis and recommended actions.
        Incident Title: {incident.get('title')}
        Description: {incident.get('description')}
        Status: {incident.get('status')}
        Severity: {incident.get('severity')}
        Recent Logs:
        {logs}

        Provide a structured analysis with:
        1. Potential root cause(s)
        2. Impact assessment
        3. Recommended immediate actions
        4. Preventive measures
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"AI analysis failed: {str(e)}"