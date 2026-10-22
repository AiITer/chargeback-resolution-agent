from app.agent.tools import get_order_details


def main() -> None:
    result = get_order_details.invoke(
        {"order_id": "ORDER-1001"}
    )

    print(result)


if __name__ == "__main__":
    main()