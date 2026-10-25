from app.integrations.easypost import get_tracking


def main() -> None:
    tracking = get_tracking("EZ4000000004")

    print("TRACKER ID:", tracking.tracker_id)
    print("TRACKING NUMBER:", tracking.tracking_number)
    print("CARRIER:", tracking.carrier)
    print("STATUS:", tracking.status)
    print("SIGNED BY:", tracking.signed_by)
    print("EST DELIVERY:", tracking.estimated_delivery_date)

    print("\nEVENTS:")

    for event in tracking.events:
        print(
            event.occurred_at,
            event.status,
            event.message,
        )


if __name__ == "__main__":
    main()