# LangGraph Series — Engineering Systems

Runnable code for the **LangGraph series** on the Engineering Systems YouTube channel. The series learns LangGraph from scratch, one working program at a time.

Each episode has its own folder. Every folder is self-contained, with its own code, tests, pinned requirements and README. You can run any episode on its own without touching the others.

## Episodes

| Episode | Folder | What you build |
| --- | --- | --- |
| 01 — Your First Working Graph | [`langgraph-ep-01/`](langgraph-ep-01/) | A two-node graph that cleans a name and greets it. It covers state, nodes, edges, partial updates, `compile()` and `invoke()`. |
| 02 — Conditional Edges | coming next | A graph that chooses its next step from the state. |

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
```

New episodes follow the same pattern: `langgraph-ep-02/`, `langgraph-ep-03/`, and so on.

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
