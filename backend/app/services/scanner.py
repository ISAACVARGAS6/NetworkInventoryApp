from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)
from ipaddress import IPv4Network, ip_network

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


def _is_gateway_candidate(ip: str, network: IPv4Network) -> bool:
    """Return whether an address is a conventional gateway candidate."""
    if network.num_addresses <= 2:
        return False

    return ip in {
        str(network.network_address + 1),
        str(network.broadcast_address - 1),
    }


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

        self.oui = oui if oui is not None else {}

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

        # A host can block ICMP while still being present on the local network.
        # The ping attempt populates the ARP cache, so a resolved MAC is a
        # second, link-layer signal that lets us retain such devices.
        mac = get_mac_address(ip)

        if not reachable and mac == "Unknown":
            return None

        hostname = get_hostname(ip)

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

        if not isinstance(target_network, IPv4Network):
            raise ValueError("Only IPv4 CIDR networks are supported")

        hosts = [
            str(ip)
            for ip in target_network.hosts()
        ]

        devices = []

        with ThreadPoolExecutor(
            max_workers=min(self.discovery_workers, max(1, len(hosts)))
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
        target_network: IPv4Network | None = None,
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
                is_gateway=(target_network is not None and _is_gateway_candidate(
                    device["ip"], target_network
                )),
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

        target_network = ip_network(network, strict=False)

        with ThreadPoolExecutor(
            max_workers=min(self.discovery_workers, max(1, len(devices)))
        ) as executor:

            futures = [
                executor.submit(
                    self.analyze_device,
                    device,
                    target_network,
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
