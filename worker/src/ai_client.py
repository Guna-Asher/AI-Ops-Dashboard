import json
import httpx


import google.generativeai as genai
from app.core.config import settings

class AIClient:
    def __init__(self):

        self._api_key = settings.GOOGLE_AI_STUDIO_API_KEY
        self._model = settings.GOOGLE_AI_STUDIO_MODEL
        self._endpoint = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')


    async def analyze_incident(self, incident: dict, logs: str) -> str:
        prompt = f"""
        Analyze the following incident and provide root cause and recommendations.
        Incident: {json.dumps(incident)}
        Logs: {logs}
        """

        if not self._api_key:
            raise RuntimeError("GOOGLE_AI_STUDIO_API_KEY is not set")

        url = self._endpoint.format(model=self._model)
        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 500,
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
        text = data["candidates"][0]["content"]["parts"][0].get("text", "")
        return (text or "").strip()

        response = self.model.generate_content(prompt)
        return response.text.strip()
