import shippo

from app.config import settings


def main() -> None:
    if not settings.shippo_api_key:
        raise RuntimeError("SHIPPO_API_KEY is not configured")

    client = shippo.Shippo(
        api_key_header=settings.shippo_api_key,
    )

    tracking = client.tracking_status.get(
        carrier="shippo",
        tracking_number="SHIPPO_RETURNED",
    )

    print("CARRIER:", tracking.carrier)
    print("TRACKING NUMBER:", tracking.tracking_number)
    print("STATUS:", tracking.tracking_status.status)
    print("DETAIL:", tracking.tracking_status.status_details)

    print("\nTRACKING HISTORY:")

    for event in tracking.tracking_history:
        print(
            event.status_date,
            event.status,
            event.status_details,
        )


if __name__ == "__main__":
    main()