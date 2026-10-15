## Agent Architecture

The system uses a durable LangGraph workflow with a ReAct-style investigation loop.

For each dispute, the agent:
- reasons over the current case state,
- dynamically selects tools such as Stripe, order, shipping, and email systems,
- retrieves relevant policy and dispute knowledge through RAG,
- reassesses the case as new evidence arrives,
- pauses and resumes for asynchronous events such as customer replies or Stripe outcomes.

Routine actions can be automated within company policy, while high-risk or exceptional cases can be escalated for human review.