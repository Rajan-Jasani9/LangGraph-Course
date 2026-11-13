# LangGraph From Scratch || Conversation Memory (Ep 05)

Checkpoints preserve graph state for a thread. MessagesState alone does not save state between invocations. InMemorySaver is volatile; SqliteSaver can recover checkpoints in another Python process.

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
python main.py --fixture --backend sqlite
python main.py "Who's handling it?" --fixture --backend sqlite
python main.py --fixture --inspect
```

`demo.py` captures real LangGraph operations with an explicitly scripted model fixture and requires no API key. Fixture answers do not establish live model behavior. The live path omits `--fixture` and requires `GROQ_API_KEY` in the environment; the default model ID is `openai/gpt-oss-20b`. The project does not automatically load a `.env` file. Never commit a key.

The local ticket and user data are illustrative. Thread IDs and user IDs are identifiers, not authorization. A service must supply authenticated identity and enforce access permissions. No remote ticket service, email service, or financial system is called.

See [EXERCISE.md](EXERCISE.md). The corresponding video timing and production notes live in the video-pipeline repository.
