import json
from app.core.config import settings

class AIClient:
    def __init__(self):
        self.api_key = settings.GOOGLE_API_KEY

    async def analyze_incident(self, incident: dict, logs: str) -> str:
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
Analyze the following incident and provide root cause and recommendations.
Incident: {json.dumps(incident)}
Logs: {logs}
"""
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"AI analysis failed: {str(e)}"