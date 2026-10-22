from app.config import settings
from app.integrations.llm import get_chat_model


def main() -> None:
    print("PROVIDER:", settings.llm_provider)
    print("MODEL:", settings.gemini_model)
    print("THINKING LEVEL:", settings.gemini_thinking_level)

    model = get_chat_model()

    response = model.invoke(
        "Reply with exactly GEMINI_OK and nothing else."
    )

    print("RESPONSE:", response.text)
    print("USAGE:", response.usage_metadata)


if __name__ == "__main__":
    main()