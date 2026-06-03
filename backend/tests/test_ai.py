import pytest
from unittest.mock import patch, AsyncMock
from app.services.ai import AIService

@pytest.mark.asyncio
async def test_ai_analysis():
    with patch("app.services.ai.httpx.AsyncClient") as mock_client:
        mock_resp = AsyncMock()
        mock_resp.json.return_value = {
            "candidates": [
                {"content": {"parts": [{"text": "Root cause: ..."}]}}
            ]
        }
        mock_resp.raise_for_status = AsyncMock()
        mock_client.return_value.__aenter__.return_value.post.return_value = mock_resp

        service = AIService()
        result = await service.analyze_incident(
            {"title": "Test", "description": "Desc", "status": "open", "severity": "high"},
            "Sample log",
        )
        assert "Root cause" in result
