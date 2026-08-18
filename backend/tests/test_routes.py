import unittest
from datetime import datetime, timezone
from unittest.mock import patch

from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api import routes_devices, routes_inventory, routes_scan
from app.core.database import Base
from app.models.device import Device
from app.models.port import Port
from app.models.scan import Scan


class RouteTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.db = self.Session()

    def tearDown(self):
        self.db.close()
        self.engine.dispose()

    def _add_device(self, ip, ports=(443, 22), device_type="Linux Server/Device"):
        scan = Scan(network="10.0.0.0/24", started_at=datetime.now(timezone.utc), finished_at=datetime.now(timezone.utc))
        device = Device(scan=scan, ip=ip, hostname="host", mac="Unknown", manufacturer="Unknown", ping_ms=None, device_type=device_type)
        for port in ports:
            device.ports.append(Port(port=port, service=str(port)))
        self.db.add(device)
        self.db.commit()
        return device

    def test_devices_are_returned_in_numeric_ip_and_port_order(self):
        self._add_device("10.0.0.100", ports=(443, 22))
        self._add_device("10.0.0.2", ports=(9100, 80))

        response = routes_devices.get_devices(self.db)

        self.assertEqual([device["ip"] for device in response], ["10.0.0.2", "10.0.0.100"])
        self.assertEqual([port["port"] for port in response[0]["ports"]], [80, 9100])

    def test_inventory_stats_counts_each_device_category(self):
        self._add_device("10.0.0.2", device_type="Windows PC/Server")
        self._add_device("10.0.0.3", device_type="Linux Server/Device")
        self._add_device("10.0.0.4", device_type="Printer")
        self._add_device("10.0.0.5", device_type="Network Infrastructure")
        self._add_device("10.0.0.6", device_type="Device/Equipment")

        self.assertEqual(
            routes_inventory.get_inventory_stats(self.db)["types"],
            {"windows": 1, "linux": 1, "servers": 0, "printers": 1, "network": 1, "unknown": 1},
        )

    def test_rejects_invalid_or_unauthorized_scan_targets(self):
        original_network = routes_scan.settings.network
        original_authorized = routes_scan.settings.authorized_networks
        original_max_hosts = routes_scan.settings.max_hosts_per_scan
        try:
            routes_scan.settings.network = "10.0.0.0/24"
            routes_scan.settings.authorized_networks = "10.0.0.0/24"
            routes_scan.settings.max_hosts_per_scan = 10
            for target, status in (("not-a-network", 400), ("10.0.1.0/30", 403), ("10.0.0.0/24", 400)):
                with self.subTest(target=target), self.assertRaises(HTTPException) as error:
                    routes_scan._validate_scan_target(target)
                self.assertEqual(error.exception.status_code, status)
        finally:
            routes_scan.settings.network = original_network
            routes_scan.settings.authorized_networks = original_authorized
            routes_scan.settings.max_hosts_per_scan = original_max_hosts

    @patch("app.api.routes_scan.NetworkScanner.scan")
    @patch("app.api.routes_scan.load_oui", return_value={})
    def test_start_scan_persists_devices_and_ports(self, _load_oui, scan):
        scan.return_value = [{
            "ip": "10.0.0.2", "hostname": "printer", "mac": "AA:BB:CC:DD:EE:FF",
            "manufacturer": "Acme", "ping_ms": 1.5, "device_type": "Printer",
            "ports": [{"port": 9100, "service": "Printer"}],
        }]
        original_network = routes_scan.settings.network
        original_authorized = routes_scan.settings.authorized_networks
        try:
            routes_scan.settings.network = "10.0.0.0/30"
            routes_scan.settings.authorized_networks = "10.0.0.0/30"
            response = routes_scan.start_scan(routes_scan.ScanRequest(), self.db)
        finally:
            routes_scan.settings.network = original_network
            routes_scan.settings.authorized_networks = original_authorized

        stored_scan = self.db.get(Scan, response["id"])
        self.assertEqual(response["hosts_found"], 1)
        self.assertEqual(stored_scan.devices[0].ports[0].port, 9100)
