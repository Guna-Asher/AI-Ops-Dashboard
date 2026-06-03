import json
from typing import Dict, Any
import google.generativeai as genai
import httpx
import google.generativeai as genai
from app.core.config import settings

class AIService:
    def __init__(self):

        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')


        if not settings.GOOGLE_AI_STUDIO_API_KEY:
            # allow startup even if key missing; actual call will fail with clear error
            self._api_key = ""
        else:
            self._api_key = settings.GOOGLE_AI_STUDIO_API_KEY

        self._model = settings.GOOGLE_AI_STUDIO_MODEL
        self._endpoint = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

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


            if not self._api_key:
                raise RuntimeError("GOOGLE_AI_STUDIO_API_KEY is not set")

            url = self._endpoint.format(model=self._model)
            payload = {
                "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.3,
                    "maxOutputTokens": 1000,
                },
            }

            async with httpx.AsyncClient(timeout=60) as client:
                resp = await client.post(
                    url,
                    params={"key": self._api_key},
                    json=payload,
                    headers={"Content-Type": "application/json"},
                )
                resp.raise_for_status()

            data = resp.json()
            # Gemini returns: candidates[0].content.parts[0].text
            text = (
                data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "")
            )
            return (text or "").strip()

            response = self.model.generate_content(prompt)
            return response.text.strip()


        except Exception as e:
            return f"AI analysis failed: {str(e)}"
