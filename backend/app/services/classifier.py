def determine_device_type(
    hostname: str,
    ports: list,
) -> str:
    """
    Classify a device using hostname and
    detected services.
    """

    hostname_lower = hostname.lower()

    port_numbers = {
        item["port"]
        for item in ports
    }

    # Printer
    if (
        9100 in port_numbers
        or any(
            keyword in hostname_lower
            for keyword in (
                "printer",
                "print",
                "impresora",
            )
        )
    ):
        return "Printer"

    # Windows
    if (
        3389 in port_numbers
        or 445 in port_numbers
    ):
        return "Windows PC/Server"

    # Linux / SSH
    if 22 in port_numbers:
        return "Linux Server/Device"

    # Server
    if any(
        keyword in hostname_lower
        for keyword in (
            "server",
            "srv",
            "servidor",
        )
    ):
        return "Server"

    # Network infrastructure
    if any(
        keyword in hostname_lower
        for keyword in (
            "router",
            "switch",
            "gateway",
            "firewall",
            "accesspoint",
            "access-point",
            "wap",
        )
    ):
        return "Network Infrastructure"

    # SNMP
    if 161 in port_numbers:
        return "Network Device"

    return "Device/Equipment"