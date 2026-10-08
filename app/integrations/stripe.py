from stripe import StripeClient

from app.config import settings


def get_stripe_client() -> StripeClient:
    if settings.stripe_secret_key is None:
        raise RuntimeError("Stripe secret key is not configured.")

    return StripeClient(settings.stripe_secret_key)

def get_stripe_balance():
    client = get_stripe_client()
    return client.v1.balance.retrieve()