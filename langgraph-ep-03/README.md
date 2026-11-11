# EP 03 — Loops and Cycles

Code for **LangGraph From Scratch || Loops and Cycles (Ep 03)** in the Engineering Systems LangGraph series.

You build a small workflow that fetches context for a support ticket from an unreliable service. When the lookup fails, the graph goes back and runs the same node again. Then you see what happens when the service never recovers, and give the graph a way to stop.

The new idea is the **cycle**: a conditional edge whose destination is a node that has already run.

No language model and no API key are needed. The service is a small simulation. Tested with Python 3.12.7 and LangGraph 1.2.20 on Windows. Python 3.11 or newer works.

## Files

```text
langgraph-ep-03/
  app/
    __init__.py
    state.py            # LookupState: ticket, attempts, success, result, available_after
    nodes.py            # fetch_context (can fail) and escalate_ticket
    routing.py          # route_after_fetch: done, escalate or retry
    graph.py            # the cycle and the escalation path
  experiments/
    single_attempt.py   # the first version, connected straight to END
    unbounded_retry.py  # a cycle with no limit, which hits the recursion limit
  tests/
    test_graph.py       # eight behaviour checks
  main.py               # command-line input, full result or node-by-node updates
  requirements.txt      # langgraph==1.2.20
  requirements-lock.txt
```

## Run it

Open a terminal in this folder, the one that contains `main.py`.

Windows PowerShell:

```powershell
python --version
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe main.py --available-after 3 --updates
```

macOS or Linux:

```bash
python3 --version
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python main.py --available-after 3 --updates
```

The same node runs three times from a single invocation:

```json
{"fetch_context": {"attempts": 1, "success": false}}
{"fetch_context": {"attempts": 2, "success": false}}
{"fetch_context": {"attempts": 3, "success": true, "result": "Ticket context retrieved."}}
```

`available_after` exists only for this simulation. It says which attempt succeeds. A real service will not tell you when it is going to recover.

To reproduce the exact tested environment, install `requirements-lock.txt` instead of `requirements.txt`.

## The cycle

```python
builder.add_conditional_edges(
    "fetch_context",
    route_after_fetch,
    {
        "done": END,
        "retry": "fetch_context",
        "escalate": "escalate_ticket",
    },
)
```

There is no Python `while` loop. The repetition comes from the edges, and the state keeps track of what has happened. That is why `fetch_context` returns the updated `attempts` on both success and failure: the next run and the router both read it.

## When the service never recovers

```powershell
.venv\Scripts\python.exe main.py --available-after 100 --updates
```

```json
{"fetch_context": {"attempts": 1, "success": false}}
{"fetch_context": {"attempts": 2, "success": false}}
{"fetch_context": {"attempts": 3, "success": false}}
{"escalate_ticket": {"result": "Support service unreachable. Ticket needs manual review."}}
```

The order of the checks in `route_after_fetch` matters. Success is checked before the attempt limit, so a third attempt that works finishes as `done` instead of being escalated.

## Without a limit

`experiments/unbounded_retry.py` is a cycle that only knows success and retry:

```powershell
.venv\Scripts\python.exe -m experiments.unbounded_retry
```

```text
GraphRecursionError: Recursion limit of 25 reached without hitting a stop condition.
```

This experiment sets `recursion_limit=25` so you reach the safeguard quickly. The default in LangGraph 1.2 is about 10,000 steps, so with that default the simulated service would simply succeed on attempt 100 before the limit is reached. The recursion limit is a safety net, not a retry plan. Decide how many retries make sense and what happens after them.

## Before you copy this pattern

- For ordinary transient failures, LangGraph also has node-level retry policies: `add_node("fetch", fetch, retry_policy=RetryPolicy(max_attempts=3))`. Build a loop when you need control over what happens between attempts, such as changing the input or trying a different tool.
- Not every operation is safe to retry. If a card charge times out, you do not know whether it went through, and running it again could charge the customer twice. Real side effects need idempotency.

## Test it

```powershell
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Expect eight passing tests.

## Troubleshooting

- `ModuleNotFoundError`: install and run with the same `.venv` interpreter.
- Imports from `app` fail: run from this folder, not from inside `app/`.

## Exercise

The maximum number of attempts is hard-coded to three in `route_after_fetch`.

1. Move that limit into the state, so different runs can use different limits.
2. Test three cases: success on the first attempt, success on the last allowed attempt, and never succeeding within the limit.
3. Pay attention to the second case. The graph should report success even on the final attempt.

**Next:** Episode 4 starts putting these concepts to work with actual tools.
