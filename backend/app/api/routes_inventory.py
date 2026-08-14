from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.device import Device
from app.models.scan import Scan


router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
)


# ============================================================
# INVENTORY SUMMARY
# ============================================================

@router.get("")
def get_inventory_summary(
    db: Session = Depends(get_db),
):
    """Return a summary of the inventory."""

    total_devices = (
        db.query(Device)
        .count()
    )

    total_scans = (
        db.query(Scan)
        .count()
    )

    return {
        "total_devices": total_devices,
        "total_scans": total_scans,
    }


# ============================================================
# INVENTORY STATISTICS
# ============================================================

@router.get("/stats")
def get_inventory_stats(
    db: Session = Depends(get_db),
):
    """Return inventory statistics."""

    devices = (
        db.query(Device)
        .all()
    )

    total_devices = len(devices)

    windows = 0
    linux = 0
    servers = 0
    printers = 0
    network_devices = 0
    unknown = 0

    for device in devices:

        device_type = (
            device.device_type
            or ""
        ).lower()

        if "windows" in device_type:
            windows += 1

        elif "linux" in device_type:
            linux += 1

        elif "server" in device_type:
            servers += 1

        elif "printer" in device_type:
            printers += 1

        elif "network" in device_type:
            network_devices += 1

        else:
            unknown += 1

    return {
        "devices": {
            "total": total_devices,
        },
        "types": {
            "windows": windows,
            "linux": linux,
            "servers": servers,
            "printers": printers,
            "network": network_devices,
            "unknown": unknown,
        },
    }