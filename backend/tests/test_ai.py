import pytest
from unittest.mock import patch, AsyncMock
from app.services.ai import AIService

@pytest.mark.asyncio
async def test_ai_analysis():
    with patch("app.services.ai.openai.AsyncOpenAI") as mock_openai:
        mock_completion = AsyncMock()
        mock_completion.choices = [AsyncMock(message=AsyncMock(content="Root cause: ..."))]
        mock_openai.return_value.chat.completions.create.return_value = mock_completion
        
        service = AIService()
        result = await service.analyze_incident(
            {"title": "Test", "description": "Desc", "status": "open", "severity": "high"},
            "Sample log"
        )
        assert "Root cause" in result