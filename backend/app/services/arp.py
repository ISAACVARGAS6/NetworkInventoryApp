import platform
import re
import subprocess


MAC_PATTERN = re.compile(
    r"([0-9a-fA-F]{2}[-:]){5}"
    r"[0-9a-fA-F]{2}"
)


def get_mac_address(ip: str) -> str:
    """
    Retrieve a MAC address from the local ARP table.

    Returns:
        MAC address or 'Unknown'.
    """

    system = platform.system().lower()

    try:
        if system == "windows":
            command = ["arp", "-a", ip]
        else:
            command = ["arp", "-n", ip]

        output = subprocess.check_output(
            command,
            encoding="utf-8",
            errors="ignore",
        )

        match = MAC_PATTERN.search(output)

        if match:
            return normalize_mac(match.group(0))

    except (
        subprocess.CalledProcessError,
        OSError,
    ):
        pass

    return "Unknown"


def normalize_mac(mac: str):
    """
    Normalize a MAC address to AA:BB:CC:DD:EE:FF.
    """

    if not mac or mac == "Unknown":
        return None

    normalized = (
        mac
        .replace("-", ":")
        .upper()
    )

    parts = normalized.split(":")

    if len(parts) != 6:
        return None

    return ":".join(parts)