from stripe import StripeClient, Webhook

from app.config import settings


def get_stripe_client() -> StripeClient:
    if settings.stripe_secret_key is None:
        raise RuntimeError("Stripe secret key is not configured.")

    return StripeClient(settings.stripe_secret_key)

def get_stripe_balance():
    client = get_stripe_client()
    return client.v1.balance.retrieve()

def construct_stripe_event(
    payload: bytes,
    signature: str | None,
):
    if settings.stripe_webhook_secret is None:
        raise RuntimeError(
            "Stripe webhook secret is not configured."
        )

    return Webhook.construct_event(
        payload=payload,
        sig_header=signature,
        secret=settings.stripe_webhook_secret,
    )