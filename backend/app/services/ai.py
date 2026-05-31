import json
from typing import Dict, Any
import openai
from app.core.config import settings

class AIService:
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

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
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1000,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"AI analysis failed: {str(e)}"