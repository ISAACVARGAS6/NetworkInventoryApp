from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.device import Device


router = APIRouter(
    prefix="/devices",
    tags=["Devices"],
)


# ============================================================
# LIST DEVICES
# ============================================================

@router.get("")
def get_devices(
    db: Session = Depends(get_db),
):
    """Return all discovered devices."""

    devices = (
        db.query(Device)
        .order_by(Device.ip)
        .all()
    )

    return [
        {
            "id": device.id,
            "scan_id": device.scan_id,
            "ip": device.ip,
            "hostname": device.hostname,
            "mac": device.mac,
            "manufacturer": device.manufacturer,
            "ping_ms": device.ping_ms,
            "device_type": device.device_type,
            "ports": [
                {
                    "port": port.port,
                    "service": port.service,
                }
                for port in device.ports
            ],
        }
        for device in devices
    ]


# ============================================================
# GET DEVICE
# ============================================================

@router.get("/{device_id}")
def get_device(
    device_id: int,
    db: Session = Depends(get_db),
):
    """Return a specific device."""

    device = (
        db.query(Device)
        .filter(Device.id == device_id)
        .first()
    )

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Device not found.",
        )

    return {
        "id": device.id,
        "scan_id": device.scan_id,
        "ip": device.ip,
        "hostname": device.hostname,
        "mac": device.mac,
        "manufacturer": device.manufacturer,
        "ping_ms": device.ping_ms,
        "device_type": device.device_type,
        "ports": [
            {
                "port": port.port,
                "service": port.service,
            }
            for port in device.ports
        ],
    }