from typing import Optional
from ipaddress import ip_address

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

    # IP addresses are stored as strings, so a database lexical sort would
    # place 192.168.1.100 before 192.168.1.2.  Sort their parsed values for
    # the order users expect in the inventory.
    devices = sorted(
        db.query(Device).all(),
        key=lambda device: ip_address(device.ip),
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
                for port in sorted(device.ports, key=lambda item: item.port)
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
            for port in sorted(device.ports, key=lambda item: item.port)
        ],
    }
