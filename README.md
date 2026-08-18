# MinutesBot — TeamSync AI

**Hackathon submission (dummy test fixture) for: AI Meeting Assistant for Automated Action Item Management**

MinutesBot ingests a meeting transcript, summarizes it, extracts action items with owners/due dates, pushes tasks to a (mocked) Planner integration, and shows everything on a local tracking dashboard.

## What actually works vs. what's mocked (intentional, for validator testing)

| Feature | Status |
|---|---|
| Transcript ingestion (`.vtt` / `.txt`) | ✅ Working |
| Summarization | ✅ Working (uses Azure OpenAI if `AZURE_OPENAI_API_KEY` is set, else falls back to a local rule-based summarizer) |
| Action item extraction | ✅ Working (rule + keyword based; not perfect — misses implicit asks) |
| Owner detection | ⚠️ Partial — works when speaker explicitly says "I'll do X" |
| Due date extraction | ⚠️ Weak — defaults to "end of week" when no date is stated |
| Planner/Jira integration | ❌ Mocked — `integrator.py` logs the payload instead of calling Microsoft Graph API |
| Reminders | ❌ Not implemented — `reminders.py` is a TODO stub |
| Dashboard | ✅ Working — Flask + SQLite, shows tasks with owner/due date/status |

This gap pattern is intentional so you can run the validator agent against a **realistic partial submission** rather than a perfect one.

## Run it

```bash
pip install -r requirements.txt
python app.py
```

Then open `http://localhost:5000` to see the dashboard, or run:

```bash
python app.py --process data/transcript_sample.vtt
```

to run the pipeline once from the command line and print the extracted action items.

## Known issue (intentional red flag for testing)
`.env.example` contains a **hardcoded-looking placeholder API key** committed to the repo — this is a deliberate security-hygiene red flag for the validator to catch, not a real credential.
