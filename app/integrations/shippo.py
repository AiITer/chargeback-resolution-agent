from datetime import datetime

import shippo
from pydantic import BaseModel

from app.config import settings


class TrackingLocationRecord(BaseModel):
    city: str | None
    state: str | None
    country: str | None
    zip: str | None


class TrackingEventRecord(BaseModel):
    status: str
    status_details: str
    occurred_at: datetime | None
    location: TrackingLocationRecord | None


class TrackingRecord(BaseModel):
    tracking_number: str
    carrier: str

    status: str
    status_details: str
    status_date: datetime | None

    eta: datetime | None

    events: list[TrackingEventRecord]


def get_tracking(
    carrier: str,
    tracking_number: str,
) -> TrackingRecord:
    if not settings.shippo_api_key:
        raise RuntimeError("SHIPPO_API_KEY is not configured")

    client = shippo.Shippo(
        api_key_header=settings.shippo_api_key,
    )

    tracking = client.tracking_status.get(
        carrier=carrier,
        tracking_number=tracking_number,
    )

    current_status = tracking.tracking_status

    if current_status is None:
        raise RuntimeError(
            f"No tracking status returned for {tracking_number}"
        )

    events: list[TrackingEventRecord] = []

    for event in tracking.tracking_history:
        location = None

        if event.location is not None:
            location = TrackingLocationRecord(
                city=event.location.city,
                state=event.location.state,
                country=event.location.country,
                zip=event.location.zip,
            )

        events.append(
            TrackingEventRecord(
                status=event.status.value,
                status_details=event.status_details,
                occurred_at=event.status_date,
                location=location,
            )
        )

    return TrackingRecord(
        tracking_number=tracking.tracking_number,
        carrier=tracking.carrier,
        status=current_status.status.value,
        status_details=current_status.status_details,
        status_date=current_status.status_date,
        eta=tracking.eta,
        events=events,
    )