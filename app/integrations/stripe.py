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

def get_stripe_dispute(dispute_id: str):
    client = get_stripe_client()
    return client.v1.disputes.retrieve(dispute_id)

def close_stripe_dispute(dispute_id: str):
    client = get_stripe_client()

    return client.v1.disputes.close(
        dispute_id
    )

def submit_stripe_dispute_evidence(
    dispute_id: str,
    *,
    uncategorized_text: str,
    shipping_carrier: str | None = None,
    shipping_tracking_number: str | None = None,
):
    client = get_stripe_client()

    evidence: dict[str, str] = {
        "uncategorized_text": uncategorized_text,
    }

    if shipping_carrier is not None:
        evidence["shipping_carrier"] = shipping_carrier

    if shipping_tracking_number is not None:
        evidence["shipping_tracking_number"] = (
            shipping_tracking_number
        )

    return client.v1.disputes.update(
        dispute_id,
        {
            "evidence": evidence,
            "submit": True,
        },
    )