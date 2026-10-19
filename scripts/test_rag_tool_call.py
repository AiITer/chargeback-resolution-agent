from langchain_core.messages import HumanMessage

from app.agent.tools import search_company_knowledge
from app.integrations.llm import get_chat_model


model = get_chat_model().bind_tools([search_company_knowledge])

messages = [
    HumanMessage(
        content=(
            "Order NS-1042 is disputed as merchandise not received. "
            "What is its current shipment status?"
        )
    )
]

response = model.invoke(messages)

print("CONTENT:", response.content)
print("TOOL CALLS:", response.tool_calls)

if response.tool_calls:
    tool_call = response.tool_calls[0]

tool_message = search_company_knowledge.invoke(tool_call)

messages.extend([
    response,
    tool_message,
])

final_response = model.invoke(messages)

print("FINAL CONTENT:")
print(final_response.content)

print("\nNEXT TOOL CALLS:")
print(final_response.tool_calls)