from langchain_core.tools import tool

from app.integrations.llm import get_chat_model


@tool
def get_order_status(order_id: str) -> str:
    """Get the current status of an order."""
    return f"Order {order_id} has been shipped."


def main() -> None:
    model = get_chat_model()
    model_with_tools = model.bind_tools([get_order_status])

    response = model_with_tools.invoke(
        "What is the current status of order ORDER-123? "
        "Use the available tool to find out."
    )

    print("TEXT:", response.text)
    print("TOOL CALLS:", response.tool_calls)
    print("USAGE:", response.usage_metadata)


if __name__ == "__main__":
    main()