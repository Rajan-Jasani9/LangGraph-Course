# EP 02 — Conditional Edges

Code for **LangGraph From Scratch || Conditional Edges (Ep 02)** in the Engineering Systems LangGraph series.
 [[Watch video on Youtube](https://youtu.be/7aaN42tgr5U)]

You build a small support-ticket router. Each ticket is classified, then sent down a different path depending on the state:

- `my app keeps crashing` goes to `technical_help`.
- `I was charged twice` goes to `billing_help`.
- `hello` matches no keyword and goes to `fallback`.

The new idea is the **conditional edge**: the graph decides which node runs next at run time, based on what is in the state.

No language model and no API key are needed. Classification is plain keyword matching so the focus stays on the graph. Tested with Python 3.12.7 and LangGraph 1.2.20 on Windows. Python 3.11 or newer works.

## Files

```text
langgraph-ep-02/
  app/
    __init__.py
    state.py          # TicketState: ticket, category, response
    nodes.py          # classify_ticket, technical_help, billing_help, fallback
    routing.py        # route_ticket: picks the path, does not update the state
    graph.py          # registers the nodes, adds the conditional edge, compiles
  experiments/
    missing_route.py  # the graph before the fallback, which fails on "hello"
  tests/
    test_graph.py     # eight behaviour checks
  main.py             # command-line input, full result or node-by-node updates
  requirements.txt    # langgraph==1.2.20
  requirements-lock.txt
```

## Run it

Open a terminal in this folder, the one that contains `main.py`.

Windows PowerShell:

```powershell
python --version
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe main.py --ticket "my app keeps crashing"
```

macOS or Linux:

```bash
python3 --version
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python main.py --ticket "my app keeps crashing"
```

Output:

```json
{
  "ticket": "my app keeps crashing",
  "category": "technical",
  "response": "Please share your error logs."
}
```

To reproduce the exact tested environment, install `requirements-lock.txt` instead of `requirements.txt`.

## See which nodes ran

Add `--updates` to print each node's update as it happens:

```powershell
.venv\Scripts\python.exe main.py --ticket "I was charged twice" --updates
```

```json
{"classify": {"category": "billing"}}
{"billing_help": {"response": "Please provide your transaction details."}}
```

`technical_help` does not appear because it never ran. LangGraph does not run every handler and then pick a response; it only executes the nodes on the selected path.

## Node or routing function?

Both are ordinary Python functions, but LangGraph treats their return values differently.

| | Registered with | Returns | LangGraph uses it to |
| --- | --- | --- | --- |
| `classify_ticket` | `add_node` | `{"category": "billing"}` | update the state |
| `route_ticket` | `add_conditional_edges` | `"billing"` | choose the next node |

Returning `"billing"` from the router does not add anything to the state. The dictionary passed to `add_conditional_edges` maps each returned label to a node, so a label does not have to match the node's name:

```python
builder.add_conditional_edges(
    "classify",
    route_ticket,
    {
        "technical": "technical_help",
        "billing": "billing_help",
        "unknown": "fallback",
    },
)
```

## Break it on purpose

`experiments/missing_route.py` is the graph before the fallback was added. The classifier assigns `unknown` to `hello`, but no destination is mapped for that label:

```powershell
.venv\Scripts\python.exe -m experiments.missing_route
```

```text
KeyError: 'unknown'
```

A fallback is a design choice. LangGraph does not add one for you. If the router returns a label that is not mapped, the run fails, and handling that case is your job. This matters more once a language model chooses the route, because a model will not always return exactly what you expected.

## Test it

```powershell
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Expect eight passing tests.

## Common confusion

- The possible paths are declared up front. Which one runs is decided only when the graph runs.
- Matching is by substring and the first matching check wins. `the invoice page shows an error` is classified as `technical`, because that check runs first. This is a deliberate simplification.
- `route_ticket` reads `category`; it does not create it. `classify_ticket` must run first.
- The graph still ends after one handler. It cannot retry or repeat a step yet.

## Troubleshooting

- `ModuleNotFoundError`: install and run with the same `.venv` interpreter.
- Imports from `app` fail: run from this folder, not from inside `app/`.
- Tickets with spaces: keep the quotes, as shown above.

## Exercise

Add a fourth route for account access.

1. Update `classify_ticket` so tickets like `I can't log in` or `I forgot my password` get a new category.
2. Create and register a new node called `account_help`.
3. Map the new label in `add_conditional_edges`, and connect `account_help` to `END`.
4. Test all four categories, not just the new one. Before each run, predict which nodes should execute, then check your prediction with `--updates`.

**Next:** [Episode 3](../langgraph-ep-03/) adds loops, so a graph can go back to an earlier node and repeat work based on a condition.
