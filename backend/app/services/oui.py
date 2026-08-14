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

                prefix = (
                    row[0]
                    .strip()
                    .upper()
                    .replace("-", ":")
                )

                manufacturer = row[1].strip()

                if len(prefix) == 8:
                    oui[prefix] = manufacturer

    except (
        OSError,
        csv.Error,
    ):
        return {}

    return oui


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