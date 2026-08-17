from datetime import datetime, timezone
from ipaddress import IPv4Network, ip_network
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.device import Device
from app.models.port import Port
from app.models.scan import Scan
from app.services.oui import load_oui
from app.services.scanner import NetworkScanner


router = APIRouter(
    prefix="/scans",
    tags=["Scans"],
)


# ============================================================
# SCHEMAS
# ============================================================

class ScanRequest(BaseModel):
    """Request model for starting a network scan."""

    network: Optional[str] = Field(
        default=None,
        description="Target network in CIDR notation.",
        examples=["192.168.1.0/24"],
    )

    discovery_timeout: Optional[int] = Field(
        default=None,
        gt=0,
        le=10000,
    )

    port_timeout: Optional[float] = Field(
        default=None,
        gt=0,
        le=10,
    )

    discovery_workers: Optional[int] = Field(
        default=None,
        ge=1,
        le=200,
    )

    port_workers: Optional[int] = Field(
        default=None,
        ge=1,
        le=200,
    )


def _validate_scan_target(network: str) -> str:
    """Validate the requested target and ensure it is operator-authorized."""
    try:
        target = ip_network(network, strict=False)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=f"Invalid network: {error}") from error

    if not isinstance(target, IPv4Network):
        raise HTTPException(status_code=400, detail="Only IPv4 CIDR networks are supported.")

    host_count = target.num_addresses if target.prefixlen >= 31 else target.num_addresses - 2
    if host_count > settings.max_hosts_per_scan:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Network contains more than {settings.max_hosts_per_scan} hosts; "
                "split it into smaller scans."
            ),
        )

    configured_networks = settings.authorized_networks or settings.network
    allowed_networks = [
        ip_network(item.strip(), strict=False)
        for item in configured_networks.split(",")
    ]
    if not any(target.subnet_of(allowed) for allowed in allowed_networks):
        raise HTTPException(status_code=403, detail="Target network is not authorized.")

    return str(target)


def _serialize_device(device: Device) -> dict:
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
            {"port": port.port, "service": port.service}
            for port in sorted(device.ports, key=lambda item: item.port)
        ],
    }


# ============================================================
# START SCAN
# ============================================================

@router.post("")
def start_scan(
    request: ScanRequest,
    db: Session = Depends(get_db),
):
    """
    Execute a network scan and persist the results.
    """

    network = _validate_scan_target(
        request.network
        or settings.network
    )

    discovery_timeout = (
        request.discovery_timeout
        if request.discovery_timeout is not None
        else settings.discovery_timeout
    )

    port_timeout = (
        request.port_timeout
        if request.port_timeout is not None
        else settings.port_timeout
    )

    discovery_workers = (
        request.discovery_workers
        if request.discovery_workers is not None
        else settings.discovery_workers
    )

    port_workers = (
        request.port_workers
        if request.port_workers is not None
        else settings.port_workers
    )

    started_at = datetime.now(timezone.utc)

    scanner = NetworkScanner(
        oui=load_oui(settings.oui_file),
        discovery_timeout=discovery_timeout,
        port_timeout=port_timeout,
        discovery_workers=discovery_workers,
        port_workers=port_workers,
    )

    # --------------------------------------------------------
    # RUN SCANNER
    # --------------------------------------------------------

    try:
        devices = scanner.scan(network)

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Scan failed: {error}",
        )

    finished_at = datetime.now(timezone.utc)

    # --------------------------------------------------------
    # CREATE SCAN
    # --------------------------------------------------------

    db_scan = Scan(
        network=network,
        status="completed",
        started_at=started_at,
        finished_at=finished_at,
        hosts_found=len(devices),
    )

    db.add(db_scan)

    # --------------------------------------------------------
    # SAVE DEVICES
    # --------------------------------------------------------

    for device_data in devices:

        db_device = Device(
            scan=db_scan,
            ip=device_data["ip"],
            hostname=device_data["hostname"],
            mac=device_data["mac"],
            manufacturer=device_data["manufacturer"],
            ping_ms=device_data["ping_ms"],
            device_type=device_data["device_type"],
        )

        db.add(db_device)

        # ----------------------------------------------------
        # SAVE PORTS
        # ----------------------------------------------------

        for port_data in device_data["ports"]:

            db_port = Port(
                device=db_device,
                port=port_data["port"],
                service=port_data["service"],
            )

            db.add(db_port)

    # --------------------------------------------------------
    # COMMIT
    # --------------------------------------------------------

    try:
        db.commit()

    except Exception as error:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {error}",
        )

    # Refresh the scan so SQLAlchemy gives us its generated ID.
    db.refresh(db_scan)

    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    return {
        "id": db_scan.id,
        "network": db_scan.network,
        "status": db_scan.status,
        "started_at": db_scan.started_at,
        "finished_at": db_scan.finished_at,
        "hosts_found": db_scan.hosts_found,
        "message": "Scan completed and saved successfully.",
    }


# ============================================================
# LIST SCANS
# ============================================================

@router.get("")
def get_scans(
    db: Session = Depends(get_db),
):
    """Return scan history."""

    scans = (
        db.query(Scan)
        .order_by(Scan.id.desc())
        .all()
    )

    return [
        {
            "id": scan.id,
            "network": scan.network,
            "status": scan.status,
            "started_at": scan.started_at,
            "finished_at": scan.finished_at,
            "hosts_found": scan.hosts_found,
        }
        for scan in scans
    ]


# ============================================================
# GET SCAN
# ============================================================

@router.get("/{scan_id}")
def get_scan(
    scan_id: int,
    db: Session = Depends(get_db),
):
    """Return a specific scan."""

    scan = (
        db.query(Scan)
        .filter(Scan.id == scan_id)
        .first()
    )

    if not scan:
        raise HTTPException(
            status_code=404,
            detail="Scan not found.",
        )

    return {
        "id": scan.id,
        "network": scan.network,
        "status": scan.status,
        "started_at": scan.started_at,
        "finished_at": scan.finished_at,
        "hosts_found": scan.hosts_found,
        "devices": [_serialize_device(device) for device in scan.devices],
    }
