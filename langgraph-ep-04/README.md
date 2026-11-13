# LangGraph From Scratch || Tool Calling (Ep 04)

Build a read-only ticket assistant with an explicit `agent → tools → agent` loop.

## Setup (PowerShell, Python 3.12)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-lock.txt
```

`requirements.txt` pins the three direct dependencies; `requirements-lock.txt` records the complete tested environment. No API key is needed for the offline tests.

```powershell
python -m unittest discover -s tests
python offline_demo.py
```

The offline demo runs **real LangGraph and ToolNode with a scripted model fixture**. Its final answers are scripted, not a captured Groq response. It tests the graph's execution paths, not model accuracy.

## Live Groq run

Get a key from the [Groq console](https://console.groq.com/keys). Set `GROQ_API_KEY` securely in your environment, then run:

```powershell
python main.py --inspect
python main.py --updates
python main.py "What does ticket priority mean?" --updates
python main.py "What's the status of ticket T-9999?" --updates
```

The default provider-qualified model ID is `openai/gpt-oss-20b`. Set `GROQ_MODEL` to use another Groq model that supports tool calling. Never commit a key. The project does not load a `.env` automatically.

`--inspect` invokes only the tool-bound model and prints its request. It does **not** run the tool. The full graph registers the tool in `ToolNode`, checks the latest AIMessage with `tools_condition`, returns the ToolMessage to `agent`, and ends when the model answers without tool calls.

The three tickets are local illustrative data. `T-1042` is in progress with the backend team; `T-2008` waits for the customer; `T-3011` is resolved. IDs include the hyphen. `T-9999` returns a normal not-found result.

`MessagesState` preserves the question, model request and paired result within an invocation. Matching message IDs can update earlier messages. No checkpointer is configured, so separate invocations do not automatically share conversation history. The CLI uses `recursion_limit=12` as an execution guard; reaching that limit is an error, not a successful answer.

## Code map

- `app/data.py`: ticket dictionary.
- `app/tools.py`: typed, documented read-only `get_ticket_status` tool.
- `app/model.py`: Groq configuration and `bind_tools`.
- `app/nodes.py`: `call_model`, created with a supplied model for testability.
- `app/graph.py`: explicit nodes and edges.
- `main.py`: live inspection, invocation and update traces.
- `offline_demo.py`: deterministic fixtures for review without provider access.

The recording says the function names in spoken camel case; the project follows Python's `get_ticket_status`, `call_model`, `bind_tools`, and `get_ticket_history` naming. “Groq” is the provider, distinct from xAI's Grok.

See [EXERCISE.md](EXERCISE.md) for the second-tool challenge. No remote repository changes or publishing are performed by this project.
