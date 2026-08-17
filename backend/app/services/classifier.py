"""
Device classification service.

Classifies discovered network devices using multiple signals:

- Hostname
- Manufacturer
- Detected TCP ports

The classifier uses a scoring system instead of relying on
a single indicator.
"""


# ============================================================
# KEYWORDS
# ============================================================

PRINTER_KEYWORDS = (
    "printer",
    "print",
    "impresora",
    "laserjet",
    "deskjet",
    "officejet",
    "plotter",
)

NETWORK_KEYWORDS = (
    "router",
    "switch",
    "gateway",
    "firewall",
    "accesspoint",
    "access-point",
    "access_point",
    "wap",
    "ap-",
    "core",
    "distribution",
    "network",
    "networking",
)

WINDOWS_KEYWORDS = (
    "windows",
    "win-",
    "win_",
    "desktop",
    "workstation",
    "pc-",
    "pc_",
    "laptop",
    "notebook",
)

LINUX_KEYWORDS = (
    "linux",
    "ubuntu",
    "debian",
    "centos",
    "rhel",
    "redhat",
    "fedora",
    "rocky",
    "almalinux",
)

SERVER_KEYWORDS = (
    "server",
    "srv",
    "servidor",
    "domain-controller",
    "domaincontroller",
    "dc-",
    "dc_",
    "nas",
)


# ============================================================
# MANUFACTURER GROUPS
# ============================================================

NETWORK_MANUFACTURERS = (
    "cisco",
    "cisco systems",
    "juniper",
    "fortinet",
    "fortigate",
    "sophos",
    "huawei",
    "mikrotik",
    "ubiquiti",
    "aruba",
    "hewlett packard enterprise",
    "hpe",
    "tp-link",
    "netgear",
    "zyxel",
    "d-link",
    "dlink",
    "meraki",
    "palo alto",
)

PRINTER_MANUFACTURERS = (
    "hp",
    "hewlett packard",
    "brother",
    "canon",
    "epson",
    "lexmark",
    "ricoh",
    "xerox",
    "kyocera",
    "konica",
)

WINDOWS_MANUFACTURERS = (
    "microsoft",
    "dell",
    "lenovo",
    "acer",
    "asus",
    "msi",
)

LINUX_MANUFACTURERS = (
    "raspberry pi",
    "raspberrypi",
    "canonical",
    "red hat",
)


# ============================================================
# HELPERS
# ============================================================

def _normalize(value: str | None) -> str:
    """
    Normalize a text value for classification.
    """
    if not value:
        return ""

    return (
        value
        .strip()
        .lower()
        .replace("_", "-")
    )


def _contains_keyword(
    value: str,
    keywords: tuple[str, ...],
) -> bool:
    """
    Check whether a normalized value contains
    at least one keyword.
    """
    return any(
        keyword in value
        for keyword in keywords
    )


def _get_port_numbers(ports: list) -> set[int]:
    """
    Extract TCP port numbers from the scanner output.
    """
    port_numbers = set()

    for item in ports or []:

        if isinstance(item, dict):

            port = item.get("port")

            if isinstance(port, int):
                port_numbers.add(port)

            elif isinstance(port, str):

                try:
                    port_numbers.add(
                        int(port)
                    )
                except ValueError:
                    continue

    return port_numbers


# ============================================================
# CLASSIFICATION
# ============================================================

def determine_device_type(
    hostname: str,
    ports: list,
    manufacturer: str = "",
    is_gateway: bool = False,
) -> str:
    """
    Classify a network device using multiple signals.

    Signals considered:

    - Hostname
    - Manufacturer
    - Open TCP ports

    Returns:
        str: Device category.
    """

    hostname_normalized = _normalize(
        hostname
    )

    manufacturer_normalized = _normalize(
        manufacturer
    )

    port_numbers = _get_port_numbers(
        ports
    )

    # --------------------------------------------------------
    # SCORES
    # --------------------------------------------------------

    scores = {
        "Printer": 0,
        "Network Infrastructure": 0,
        "Windows PC/Server": 0,
        "Linux Server/Device": 0,
        "Server": 0,
    }

    # ========================================================
    # PRINTER
    # ========================================================

    if 9100 in port_numbers:
        scores["Printer"] += 6

    if 161 in port_numbers and 9100 in port_numbers:
        scores["Printer"] += 2

    if _contains_keyword(
        hostname_normalized,
        PRINTER_KEYWORDS,
    ):
        scores["Printer"] += 5

    if _contains_keyword(
        manufacturer_normalized,
        PRINTER_MANUFACTURERS,
    ):
        scores["Printer"] += 3


    # ========================================================
    # NETWORK INFRASTRUCTURE
    # ========================================================

    if _contains_keyword(
        hostname_normalized,
        NETWORK_KEYWORDS,
    ):
        scores["Network Infrastructure"] += 5

    if _contains_keyword(
        manufacturer_normalized,
        NETWORK_MANUFACTURERS,
    ):
        scores["Network Infrastructure"] += 5

    # The usual first/last usable address is not proof on its own, but it is
    # a strong useful signal when a gateway does not expose a management port
    # or reply to reverse DNS.
    if is_gateway:
        scores["Network Infrastructure"] += 6

    if 161 in port_numbers:
        scores["Network Infrastructure"] += 4

    if 23 in port_numbers:
        scores["Network Infrastructure"] += 4

    if (
        22 in port_numbers
        and (
            80 in port_numbers
            or 443 in port_numbers
        )
        and 161 in port_numbers
    ):
        scores["Network Infrastructure"] += 3


    # ========================================================
    # WINDOWS
    # ========================================================

    if 3389 in port_numbers:
        scores["Windows PC/Server"] += 5

    if 445 in port_numbers:
        scores["Windows PC/Server"] += 4

    if 5985 in port_numbers:
        scores["Windows PC/Server"] += 4

    if 5986 in port_numbers:
        scores["Windows PC/Server"] += 4

    if _contains_keyword(
        hostname_normalized,
        WINDOWS_KEYWORDS,
    ):
        scores["Windows PC/Server"] += 3

    if _contains_keyword(
        manufacturer_normalized,
        WINDOWS_MANUFACTURERS,
    ):
        scores["Windows PC/Server"] += 1


    # ========================================================
    # LINUX
    # ========================================================

    if 22 in port_numbers:
        scores["Linux Server/Device"] += 4

    if _contains_keyword(
        hostname_normalized,
        LINUX_KEYWORDS,
    ):
        scores["Linux Server/Device"] += 5

    if _contains_keyword(
        manufacturer_normalized,
        LINUX_MANUFACTURERS,
    ):
        scores["Linux Server/Device"] += 3

    if (
        22 in port_numbers
        and (
            80 in port_numbers
            or 443 in port_numbers
        )
    ):
        scores["Linux Server/Device"] += 1


    # ========================================================
    # SERVER
    # ========================================================

    if _contains_keyword(
        hostname_normalized,
        SERVER_KEYWORDS,
    ):
        scores["Server"] += 6

    if (
        22 in port_numbers
        and 443 in port_numbers
    ):
        scores["Server"] += 2

    if (
        445 in port_numbers
        and (
            3389 in port_numbers
            or 5985 in port_numbers
            or 5986 in port_numbers
        )
    ):
        scores["Server"] += 2


    # ========================================================
    # RESULT
    # ========================================================

    best_type = max(
        scores,
        key=scores.get,
    )

    best_score = scores[best_type]

    if best_score == 0:
        return "Device/Equipment"

    return best_type
