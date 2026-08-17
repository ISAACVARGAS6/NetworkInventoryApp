import platform
import re
import subprocess


def ping_host(ip: str, timeout_ms: int = 500):
    """
    Ping a host and return its reachability and RTT.

    Returns:
        tuple[bool, float | None]:
            (reachable, ping_time_ms)
    """

    system = platform.system().lower()

    if system == "windows":
        command = [
            "ping",
            "-n",
            "1",
            "-w",
            str(timeout_ms),
            ip,
        ]
    else:
        timeout_seconds = max(1, int(timeout_ms / 1000))

        command = [
            "ping",
            "-c",
            "1",
            "-W",
            str(timeout_seconds),
            ip,
        ]

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            encoding="utf-8",
            errors="ignore",
            check=False,
            timeout=max(2, (timeout_ms / 1000) + 2),
        )

    except (OSError, subprocess.TimeoutExpired):
        return False, None

    if result.returncode != 0:
        return False, None

    output = result.stdout

    pattern = (
        r"(?:time|tiempo)[=<]\s*"
        r"(\d+(?:\.\d+)?)\s*ms"
    )

    match = re.search(
        pattern,
        output,
        re.IGNORECASE,
    )

    if match:
        return True, float(match.group(1))

    return True, None
