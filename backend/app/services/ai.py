import json
from typing import Dict, Any
from app.core.config import settings

class AIService:
    def __init__(self):
        self.api_key = settings.GOOGLE_API_KEY

    async def analyze_incident(self, incident: Dict[str, Any], logs: str) -> str:
        """
        Returns a dummy analysis when GOOGLE_API_KEY is 'dummy' or empty,
        otherwise calls Google Generative AI.
        """
        # ---------- DUMMY MODE ----------
        if not self.api_key or self.api_key == "dummy":
            return (
                "DUMMY AI ANALYSIS (replace GOOGLE_API_KEY with a real key)\n\n"
                f"Root Cause: Simulated root cause for incident '{incident.get('title', 'Unknown')}'.\n"
                f"Impact Assessment: Severity {incident.get('severity', 'unknown')} could affect system performance.\n"
                "Immediate Actions: Check logs, restart affected service, notify on-call.\n"
                "Preventive Measures: Set up monitoring alerts and auto-scaling."
            )
        # ---------- REAL API CALL ----------
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
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
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"AI analysis failed: {str(e)}"