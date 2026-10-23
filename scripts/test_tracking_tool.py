from app.agent.tools import get_tracking_details


def main() -> None:
    result = get_tracking_details.invoke(
        {
            "carrier": "shippo",
            "tracking_number": "SHIPPO_FAILURE",
        }
    )

    print(result)


if __name__ == "__main__":
    main()