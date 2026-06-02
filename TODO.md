# TODO - Google AI Studio (Gemini) migration

## Step 1
- Replace OpenAI settings with Google AI Studio env vars in `backend/app/core/config.py`.

## Step 2
- Rewrite `backend/app/services/ai.py` to call Gemini REST using `GOOGLE_AI_STUDIO_API_KEY`.

## Step 3
- Rewrite `worker/src/ai_client.py` similarly.

## Step 4
- Remove `openai` dependency and add/keep required deps in:
  - `backend/requirements.txt`
  - `worker/requirements.txt`

## Step 5
- Update unit test `backend/tests/test_ai.py` to mock the HTTP request.

## Step 6
- Update `.env.example` to expose `GOOGLE_AI_STUDIO_API_KEY` and `GOOGLE_AI_STUDIO_MODEL`.

## Step 7
- Run backend tests: `pytest`.

