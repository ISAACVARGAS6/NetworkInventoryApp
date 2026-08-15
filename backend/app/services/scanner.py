from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)
from ipaddress import ip_network

from app.services.arp import get_mac_address
from app.services.classifier import (
    determine_device_type,
)
from app.services.dns import get_hostname
from app.services.oui import (
    get_manufacturer,
)
from app.services.ping import ping_host
from app.services.ports import scan_ports


class NetworkScanner:
    """
    Network discovery and inventory scanner.
    """

    def __init__(
        self,
        oui: dict | None = None,
        discovery_timeout: int = 500,
        port_timeout: float = 0.25,
        discovery_workers: int = 50,
        port_workers: int = 30,
    ):

        self.oui = oui or {}

        self.discovery_timeout = (
            discovery_timeout
        )

        self.port_timeout = port_timeout

        self.discovery_workers = (
            discovery_workers
        )

        self.port_workers = port_workers

    # ========================================================
    # DISCOVER HOST
    # ========================================================

    def discover_host(
        self,
        ip: str,
    ):
        """Discover basic information about one host."""

        reachable, ping_ms = ping_host(
            ip,
            self.discovery_timeout,
        )

        if not reachable:
            return None

        hostname = get_hostname(ip)

        mac = get_mac_address(ip)

        manufacturer = get_manufacturer(
            mac,
            self.oui,
        )

        return {
            "ip": ip,
            "hostname": hostname,
            "mac": mac,
            "manufacturer": manufacturer,
            "ping_ms": ping_ms,
            "device_type": None,
            "ports": [],
        }

    # ========================================================
    # DISCOVER NETWORK
    # ========================================================

    def discover_network(
        self,
        network: str,
    ) -> list:
        """
        Discover active hosts in a CIDR network.
        """

        target_network = ip_network(
            network,
            strict=False,
        )

        hosts = [
            str(ip)
            for ip in target_network.hosts()
        ]

        devices = []

        with ThreadPoolExecutor(
            max_workers=self.discovery_workers
        ) as executor:

            futures = {
                executor.submit(
                    self.discover_host,
                    ip,
                ): ip
                for ip in hosts
            }

            for future in as_completed(futures):

                try:
                    device = future.result()

                    if device:
                        devices.append(device)

                except Exception:
                    continue

        devices.sort(
            key=lambda device: tuple(
                int(part)
                for part in device["ip"].split(".")
            )
        )

        return devices

    # ========================================================
    # ANALYZE DEVICE
    # ========================================================

    def analyze_device(
        self,
        device: dict,
    ):
        """Scan ports and classify a device."""

        ports = scan_ports(
            device["ip"],
            timeout=self.port_timeout,
            max_workers=self.port_workers,
        )

        device["ports"] = ports

        device["device_type"] = (
            determine_device_type(
                device["hostname"],
                ports=ports,
                manufacturer=device["manufacturer"],
            )
        )

        return device

    # ========================================================
    # FULL SCAN
    # ========================================================

    def scan(
        self,
        network: str,
    ) -> list:
        """
        Perform complete network discovery
        and device analysis.
        """

        devices = self.discover_network(
            network
        )

        with ThreadPoolExecutor(
            max_workers=self.discovery_workers
        ) as executor:

            futures = [
                executor.submit(
                    self.analyze_device,
                    device,
                )
                for device in devices
            ]

            analyzed_devices = []

            for future in as_completed(futures):

                try:
                    device = future.result()

                    analyzed_devices.append(
                        device
                    )

                except Exception:
                    continue

        analyzed_devices.sort(
            key=lambda device: tuple(
                int(part)
                for part in device["ip"].split(".")
            )
        )

        return analyzed_devices