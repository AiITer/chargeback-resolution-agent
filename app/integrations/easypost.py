from datetime import datetime

import easypost
from pydantic import BaseModel

from app.config import settings


class TrackingLocationRecord(BaseModel):
    city: str | None
    state: str | None
    country: str | None
    zip: str | None


class TrackingEventRecord(BaseModel):
    status: str
    status_detail: str | None
    message: str | None
    occurred_at: datetime
    source: str | None
    location: TrackingLocationRecord | None


class TrackingRecord(BaseModel):
    tracker_id: str
    tracking_number: str
    carrier: str
    status: str
    status_detail: str | None

    signed_by: str | None
    estimated_delivery_date: datetime | None
    shipment_id: str | None

    events: list[TrackingEventRecord]


def get_tracking(tracking_number: str) -> TrackingRecord:
    if not settings.easypost_api_key:
        raise RuntimeError("EASYPOST_API_KEY is not configured")

    client = easypost.EasyPostClient(
        settings.easypost_api_key
    )

    tracker = client.tracker.create(
        tracking_code=tracking_number
    )

    events: list[TrackingEventRecord] = []

    for detail in tracker.tracking_details:
        location = None

        if detail.tracking_location is not None:
            location = TrackingLocationRecord(
                city=detail.tracking_location.city,
                state=detail.tracking_location.state,
                country=detail.tracking_location.country,
                zip=detail.tracking_location.zip,
            )

        events.append(
            TrackingEventRecord(
                status=detail.status,
                status_detail=detail.status_detail,
                message=detail.message,
                occurred_at=detail.datetime,
                source=detail.source,
                location=location,
            )
        )

    return TrackingRecord(
        tracker_id=tracker.id,
        tracking_number=tracker.tracking_code,
        carrier=tracker.carrier,
        status=tracker.status,
        status_detail=tracker.status_detail,
        signed_by=tracker.signed_by,
        estimated_delivery_date=tracker.est_delivery_date,
        shipment_id=tracker.shipment_id,
        events=events,
    )