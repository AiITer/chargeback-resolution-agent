from app.integrations.order_service import get_order


def main() -> None:
    order = get_order("ORDER-1001")

    print("ORDER ID:", order.order_id)
    print("STATUS:", order.status)
    print("FULFILLMENT:", order.fulfillment_status)
    print(order.shipping_carrier)
    print("TRACKING:", order.tracking_number)
    print("REFUND STATUS:", order.refund_status)
    print("REFUNDED AT:", order.refunded_at)


if __name__ == "__main__":
    main()