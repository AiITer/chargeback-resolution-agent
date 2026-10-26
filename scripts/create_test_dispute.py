from datetime import datetime, timedelta, timezone

from app.integrations.order_service import (
    create_order,
    update_order_fulfillment,
    update_order_refund,
    update_order_status,
    update_order_stripe_references,
)
from app.integrations.stripe import get_stripe_client

import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--refund",
        action="store_true",
    )
    parser.add_argument(
        "--human-review",
        action="store_true",
    )
    args = parser.parse_args()

    story_now = datetime.now(timezone.utc)
    story_now = datetime.now(timezone.utc)

    order_created_at = story_now - timedelta(days=7)
    refunded_at = story_now - timedelta(hours=1)
    client = get_stripe_client()

    payment_intent = client.v1.payment_intents.create(
        {
            "amount": 1800,
            "currency": "cad",
            "payment_method": "pm_card_createDisputeProductNotReceived",
            "automatic_payment_methods": {
                "enabled": True,
                "allow_redirects": "never",
            },
        }
    )

    print("PAYMENT INTENT:", payment_intent.id)

    order = create_order(
        customer_id="CUSTOMER-1001",
        amount=payment_intent.amount,
        currency=payment_intent.currency,
        payment_intent_id=payment_intent.id,
        created_at=order_created_at,
    )

    print("ORDER CREATED:", order.order_id)

    payment_intent = client.v1.payment_intents.confirm(
        payment_intent.id
    )

    print("PAYMENT STATUS:", payment_intent.status)
    print("CHARGE:", payment_intent.latest_charge)

    update_order_stripe_references(
        order.order_id,
        charge_id=payment_intent.latest_charge,
    )

    if payment_intent.status == "succeeded":
        update_order_status(
            order.order_id,
            status="paid",
        )

        update_order_fulfillment(
            order.order_id,
            fulfillment_status=(
                "delivered"
                if args.human_review
                else "shipped"
            ),
            shipping_carrier="shippo",
            tracking_number="SHIPPO_FAILURE",
        )

    if args.refund:
        update_order_refund(
            order.order_id,
            refund_status="refunded",
            refund_amount=payment_intent.amount,
            refunded_at=refunded_at,
        )

        print("ORDER UPDATED WITH PRIOR REFUND")

    print("ORDER UPDATED WITH CHARGE")


if __name__ == "__main__":
    main()