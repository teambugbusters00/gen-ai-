# GenAI Playground

A practical playground for experimenting with generative AI workflows.

## MVP
- Prompt templates with reusable variables
- Local JSON prompt library
- Python CLI to list, inspect, and run templates against an OpenAI-compatible chat endpoint

## Setup
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
python app.py list
```

Set `AI_BASE_URL`, `AI_API_KEY`, and `AI_MODEL` in `.env` before calling the model. Never commit real API keys.

## Status
Starter MVP; provider calls require a compatible endpoint and credentials.
