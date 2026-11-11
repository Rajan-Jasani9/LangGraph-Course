# EP 01 — Your First Working Graph

Code for **LangGraph From Scratch || Your First Working Graph (Ep 01)** in the Engineering Systems LangGraph series. [Watch on YouTube](https://youtu.be/Xjvp9MvAPcM).

You build a small workflow that takes a name, cleans it, and produces a greeting. The problem is deliberately tiny so you can watch how information moves between nodes:

- **State** carries the information: `raw_name`, then `name`, then `greeting`.
- **Nodes** do the work: `clean_name` and `greet` are ordinary Python functions.
- **Edges** decide the order: `START → clean_name → greet → END`.

No language model and no API key are needed. Tested with Python 3.12.7 and LangGraph 1.2.20 on Windows. Python 3.11 or newer works.

## Files

```text
langgraph-ep-01/
  app/
    __init__.py
    state.py          # GreetingState: the shape of the shared state
    nodes.py          # clean_name and greet, two plain Python functions
    graph.py          # registers the nodes, connects the edges, compiles the graph
  tests/
    test_graph.py     # six behaviour checks
  main.py             # command-line input, invoke or trace, printed output
  requirements.txt    # langgraph==1.2.20
  requirements-lock.txt
```

The files were written in the same order as in the video: `state.py`, `nodes.py`, `graph.py`, then `main.py`.

## Run it

Open a terminal in this folder, the one that contains `main.py`.

Windows PowerShell:

```powershell
python --version
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe main.py --name "  Rajan  "
```

macOS or Linux:

```bash
python3 --version
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python main.py --name "  Rajan  "
```

Output:

```json
{
  "raw_name": "  Rajan  ",
  "name": "Rajan",
  "greeting": "Hello, Rajan!"
}
```

`raw_name` keeps its spaces. `clean_name` returned only `name`, and LangGraph merged that update into the existing state instead of replacing it.

To reproduce the exact tested environment, install `requirements-lock.txt` instead of `requirements.txt`.

## Follow the state

Add `--trace` to print the full state after each step of a new run:

```powershell
.venv\Scripts\python.exe main.py --name "  Rajan  " --trace
```

```json
{"raw_name": "  Rajan  "}
{"raw_name": "  Rajan  ", "name": "Rajan"}
{"raw_name": "  Rajan  ", "name": "Rajan", "greeting": "Hello, Rajan!"}
```

This uses `graph.stream(..., stream_mode="values")`, which yields full state snapshots for this sequential graph. Streaming starts a new run; it does not inspect an earlier `invoke` call.

## Try it and test it

```powershell
.venv\Scripts\python.exe main.py --name "  Mira  "
.venv\Scripts\python.exe main.py --name "   "
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Expect `Hello, Mira!`, then `Hello, friend!` (the fallback for a blank name), then six passing tests.

## Common confusion

- `TypedDict` describes types; it does not validate input at runtime. `NotRequired` means a key may be absent, not that its value is `None`.
- A node returns only the fields it changes. Plain string updates replace those keys and keep the rest. Lists need a reducer when you want them to accumulate.
- Pass `clean_name` to `add_node` without `()`. You register the function; LangGraph calls it later.
- `compile()` prepares the graph. `invoke()` runs it.
- Edges set the order. Declaring `name` in the schema does not create it. Skip `clean_name` and `greet` fails with `KeyError: 'name'`.
- There is no checkpointer or store here, so nothing persists between runs.
- This is a fixed, deterministic workflow, not an agent. LangGraph itself is not a language model.

## Troubleshooting

- `ModuleNotFoundError`: install and run with the same `.venv` interpreter.
- Imports from `app` fail: run from this folder, not from inside `app/`.
- Names with spaces: keep the quotes, as shown above.
- No environment activation or PowerShell policy change is needed.

## Exercise

1. Recreate `app/graph.py` from memory: register both nodes and add the three edges.
2. Change the greeting prefix from `Hello` to `Welcome`, then update the expected greetings in `tests/test_graph.py`.
3. Explain why `raw_name` is still in the final result, even though `clean_name` returned only `name`.

**Next:** [EP 02](../langgraph-ep-02/) adds conditional edges, so the graph can choose its next step from the state.
