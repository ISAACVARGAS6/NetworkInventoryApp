import csv
import os


def load_oui(file_path: str):
    """
    Load OUI information from CSV.

    Expected format:

        OUI,Manufacturer
        AA:BB:CC,Example Manufacturer
    """

    oui = {}

    if not os.path.exists(file_path):
        return oui

    try:
        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as file:

            reader = csv.reader(file)

            for row in reader:

                if len(row) < 2:
                    continue

                prefix = _normalize_oui_prefix(row[0])

                manufacturer = row[1].strip()

                if prefix:
                    oui[prefix] = manufacturer

    except (
        OSError,
        csv.Error,
    ):
        return {}

    return oui


def _normalize_oui_prefix(value: str) -> str | None:
    """Return an OUI as ``AA:BB:CC`` from common source formats."""
    compact = "".join(char for char in value if char.isalnum()).upper()
    if len(compact) != 6 or any(char not in "0123456789ABCDEF" for char in compact):
        return None
    return ":".join((compact[0:2], compact[2:4], compact[4:6]))


def get_manufacturer(mac: str, oui: dict) -> str:
    """
    Identify manufacturer using the MAC OUI.
    """

    if not mac or mac == "Unknown":
        return "Unknown"

    normalized = (
        mac
        .replace("-", ":")
        .upper()
    )

    parts = normalized.split(":")

    if len(parts) != 6:
        return "Unknown"

    prefix = ":".join(parts[:3])

    return oui.get(
        prefix,
        "Unknown",
    )
