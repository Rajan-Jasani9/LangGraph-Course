# Add a second read-only tool

1. Create a `HISTORY` dictionary keyed by ticket ID. For `T-1042`, use illustrative updates: created Monday, assigned Tuesday, in progress Wednesday.
2. Define `@tool def get_ticket_history(ticket_id: str) -> dict`. Write a docstring that distinguishes history from current status. Return an explicit not-found result for missing tickets.
3. Pass **the same two-tool list** to both `make_model(tools=...)` and `build_graph(model, tools=...)`. Binding a schema and registering execution are separate steps.
4. Extend the system instruction to request history when needed and avoid inventing events.
5. Inspect actual `tool_calls` for current status, history, and a combined question. The model might request two tools in one response or in successive turns. Do not assert a particular call order as universal behavior.

Test prompts:

```text
What's the current status of T-1042?
What happened to T-1042 before that?
What's the current status of T-1042, and what happened to it before that?
```

For the standalone history prompt, specify the ticket ID explicitly; no memory across invocations is configured yet. Check that result IDs match tool-call IDs and both requested results reach the next model turn. Test an unknown ticket and a general non-ticket question too.

Exit check: explain why adding `get_ticket_history` to `bind_tools` alone does not execute it, and why adding it only to `ToolNode` does not advertise it to the model.
