# LangGraph Series — Engineering Systems

Runnable code for the **LangGraph series** on the Engineering Systems YouTube channel. The series learns LangGraph from scratch, one working program at a time.

Each episode has its own folder. Every folder is self-contained, with its own code, tests, pinned requirements and README. You can run any episode on its own without touching the others.

## Episodes

| Episode | Video | Folder | What you build |
| --- | --- | --- | --- |
| 01 — Your First Working Graph | [Watch on YouTube](https://youtu.be/Xjvp9MvAPcM) | [`langgraph-ep-01/`](langgraph-ep-01/) | A two-node graph that cleans a name and greets it. It covers state, nodes, edges, partial updates, `compile()` and `invoke()`. |
| 02 — Conditional Edges | [Watch on Youtube](https://youtu.be/7aaN42tgr5U) | [`langgraph-ep-02/`](langgraph-ep-02/) | A support-ticket router that picks its next node from the state. It covers conditional edges, routing functions, path maps, and handling an unmapped route with a fallback. |
| 03 — Loops and Cycles | coming soon | [`langgraph-ep-03/`](langgraph-ep-03/) | A retry workflow that goes back to a node it already ran. It covers cycles, retry limits, the recursion limit, and escalating when the retries run out. |
| 04 — Tool Calling | in production | [`langgraph-ep-04/`](langgraph-ep-04/) | A read-only ticket assistant using ChatGroq, MessagesState, ToolNode and tools_condition. Includes live CLI commands, explicit offline fixtures, tests, and a second-tool exercise. |
| 05 — Conversation Memory | in production | [`langgraph-ep-05/`](langgraph-ep-05/) | Thread-scoped checkpoints, state inspection, and SQLite recovery after a process restart. |
| 06 — Long-Term Memory | in production | [`langgraph-ep-06/`](langgraph-ep-06/) | User namespaces, ToolRuntime, saved preferences and explicit retrieval across conversations. |
| 07 — Human in the Loop | in production | [`langgraph-ep-07/`](langgraph-ep-07/) | Pause before a local ticket-priority write, inspect the proposal, and resume with approval or rejection. |

## Repository layout

```text
Langgraph/
  README.md              # this file: series overview and episode index
  .gitignore
  langgraph-ep-01/       # one folder per episode
    README.md            # how to run that episode, and its exercise
    app/                 # the episode's graph code
    tests/
    main.py
    requirements.txt     # the direct dependency the episode was tested with
    requirements-lock.txt
  langgraph-ep-02/       # same layout, plus experiments/ for the failure shown in the video
```

New episodes follow the same pattern: `langgraph-ep-04/`, `langgraph-ep-05/`, and so on.

## Running an episode

You need Python 3.11 or newer. Work inside the episode's folder and give each episode its own virtual environment, because later episodes may pin different versions.

On Windows PowerShell:

```powershell
cd langgraph-ep-01
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe main.py
```

On macOS or Linux:

```bash
cd langgraph-ep-01
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python main.py
```

Each episode README has the exact commands, the expected output, and the exercise from the video.

## Notes

- Early episodes need no model API key. When a later episode does, its README says so. Keep keys in a local `.env` file, which `.gitignore` excludes.
- This is an independent tutorial series. The LangGraph and LangChain names identify the frameworks being taught and do not imply sponsorship or endorsement.
- Framework docs: <https://docs.langchain.com/oss/python/langgraph/overview>
