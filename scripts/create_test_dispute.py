from app.integrations.stripe import get_stripe_client


def main():
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
        "confirm": True,
    }
)
    print(payment_intent.id)


if __name__ == "__main__":
    main()