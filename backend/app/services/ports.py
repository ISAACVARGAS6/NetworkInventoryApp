import socket
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)


DEFAULT_PORTS = {
    22: "SSH",
    23: "Telnet",
    80: "HTTP",
    161: "SNMP",
    443: "HTTPS",
    445: "SMB",
    3389: "RDP",
    5985: "WinRM",
    5986: "WinRM HTTPS",
    9100: "Printer",
}


def check_port(
    ip: str,
    port: int,
    timeout: float = 0.25,
) -> bool:
    """Check whether a TCP port is accepting connections."""

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
    )

    sock.settimeout(timeout)

    try:
        return sock.connect_ex(
            (ip, port)
        ) == 0

    except OSError:
        return False

    finally:
        sock.close()


def scan_ports(
    ip: str,
    ports=None,
    timeout: float = 0.25,
    max_workers: int = 30,
) -> list:
    """
    Scan configured TCP ports.

    Returns:
        List of dictionaries containing
        port and service information.
    """

    if ports is None:
        ports = DEFAULT_PORTS

    open_ports = []

    with ThreadPoolExecutor(
        max_workers=max_workers
    ) as executor:

        futures = {
            executor.submit(
                check_port,
                ip,
                port,
                timeout,
            ): (
                port,
                service,
            )
            for port, service in ports.items()
        }

        for future in as_completed(futures):

            port, service = futures[future]

            try:
                if future.result():
                    open_ports.append(
                        {
                            "port": port,
                            "service": service,
                        }
                    )

            except Exception:
                continue

    open_ports.sort(
        key=lambda item: item["port"]
    )

    return open_ports