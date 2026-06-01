import openai
from app.core.config import settings

class AIClient:
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def analyze_incident(self, incident: dict, logs: str) -> str:
        prompt = f"""
        Analyze the following incident and provide root cause and recommendations.
        Incident: {json.dumps(incident)}
        Logs: {logs}
        """
        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500,
        )
        return response.choices[0].message.content.strip()