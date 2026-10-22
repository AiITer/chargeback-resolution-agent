from app.integrations.shippo import get_tracking


def main() -> None:
    tracking = get_tracking(
        carrier="shippo",
        tracking_number="SHIPPO_DELIVERED",
    )

    print("TRACKING NUMBER:", tracking.tracking_number)
    print("CARRIER:", tracking.carrier)
    print("STATUS:", tracking.status)
    print("DETAIL:", tracking.status_details)
    print("STATUS DATE:", tracking.status_date)
    print("ETA:", tracking.eta)

    print("\nEVENTS:")

    for event in tracking.events:
        print(
            event.occurred_at,
            event.status,
            event.status_details,
        )


if __name__ == "__main__":
    main()