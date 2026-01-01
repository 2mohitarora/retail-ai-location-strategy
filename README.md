# retail-ai-location-strategy
This uses Claude Agent SDK, Equivalent version using Google Agent SDK is built for comparsion. Source code of that is available here: https://github.com/2mohitarora/adventofagents/tree/main/retail-location-strategy 

## What it does 
Given a location and business type, this pipeline automatically:

Researches the market using live web search
Maps competitors using Google Maps Places API
Calculates viability scores with Python code execution
Generates strategic recommendations with extended reasoning
Produces an HTML executive report and visual infographic

### Setup Environment
```bash
uv init
uv add claude-agent-sdk
source .venv/bin/activate
uv run main.py
```