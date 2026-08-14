import socket


def get_hostname(ip: str) -> str:
    """
    Resolve an IP address to a hostname.

    Returns:
        Hostname or 'No DNS'.
    """

    try:
        return socket.gethostbyaddr(ip)[0]

    except (
        socket.herror,
        socket.gaierror,
        OSError,
    ):
        return "No DNS"