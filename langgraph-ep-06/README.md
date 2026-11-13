# LangGraph From Scratch || Long-Term Memory (Ep 06)

A store holds explicitly selected user data outside thread state. ToolRuntime supplies application-controlled identity and storage. A later node retrieves the preference into the model input. InMemoryStore spans threads in one process but does not survive a fresh process.

## Setup

Tested with Python 3.12, LangGraph 1.2.20, langchain-core 1.8.0, langchain-groq 1.1.3 and langgraph-checkpoint-sqlite 3.1.3. Use a separate environment:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.venv\Scripts\python.exe -B -m unittest discover -s tests
.venv\Scripts\python.exe -B demo.py
```

After activating the environment, the main example is:

```powershell
python main.py --fixture
```

`demo.py` captures real LangGraph operations with an explicitly scripted model fixture and requires no API key. Fixture answers do not establish live model behavior. The live path omits `--fixture` and requires `GROQ_API_KEY` in the environment; the default model ID is `openai/gpt-oss-20b`. The project does not automatically load a `.env` file. Never commit a key.

The local ticket and user data are illustrative. Thread IDs and user IDs are identifiers, not authorization. A service must supply authenticated identity and enforce access permissions. No remote ticket service, email service, or financial system is called.

See [EXERCISE.md](EXERCISE.md). The corresponding video timing and production notes live in the video-pipeline repository.

The runtime argument is hidden from the model-facing `tool_call_schema`. User preferences are data; production systems need a deliberate policy for potentially hostile stored text. The store in this lesson is deliberately volatile.
