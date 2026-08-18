import subprocess
import unittest
from unittest.mock import MagicMock, patch

from app.services.arp import get_mac_address, normalize_mac
from app.services.classifier import determine_device_type
from app.services.oui import _normalize_oui_prefix, get_manufacturer, load_oui
from app.services.ping import ping_host
from app.services.ports import scan_ports
from app.services.scanner import NetworkScanner, _is_gateway_candidate


class ClassifierTests(unittest.TestCase):
    def test_classifies_devices_from_multiple_signals(self):
        cases = (
            ("laserjet-floor-2", [{"port": 9100}, {"port": 161}], "", False, "Printer"),
            ("", [{"port": 22}, {"port": 80}, {"port": 161}], "Cisco Systems", False, "Network Infrastructure"),
            ("pc-alice", [{"port": 445}, {"port": 3389}], "Dell", False, "Windows PC/Server"),
            ("ubuntu-build", [{"port": 22}, {"port": 443}], "", False, "Linux Server/Device"),
            ("unidentified", [], "", False, "Device/Equipment"),
        )

        for hostname, ports, manufacturer, is_gateway, expected in cases:
            with self.subTest(hostname=hostname, expected=expected):
                self.assertEqual(
                    determine_device_type(hostname, ports, manufacturer, is_gateway),
                    expected,
                )

    def test_gateway_is_network_infrastructure_without_other_signals(self):
        self.assertEqual(
            determine_device_type("", [], is_gateway=True),
            "Network Infrastructure",
        )

    def test_ignores_invalid_port_values(self):
        self.assertEqual(
            determine_device_type("", [{"port": "not-a-port"}, None, {}]),
            "Device/Equipment",
        )


class NetworkUtilityTests(unittest.TestCase):
    def test_normalize_mac_accepts_common_format_and_rejects_malformed_values(self):
        self.assertEqual(normalize_mac("aa-bb-cc-dd-ee-ff"), "AA:BB:CC:DD:EE:FF")
        self.assertIsNone(normalize_mac("aa:bb:cc:dd:ee:gg"))
        self.assertIsNone(normalize_mac("a:bb:cc:dd:ee:ff"))

    @patch("app.services.arp.subprocess.check_output")
    @patch("app.services.arp.platform.system", return_value="Windows")
    def test_get_mac_address_parses_arp_output(self, _system, check_output):
        check_output.return_value = "  192.168.1.10  aa-bb-cc-dd-ee-ff  dynamic"
        self.assertEqual(get_mac_address("192.168.1.10"), "AA:BB:CC:DD:EE:FF")
        check_output.assert_called_once_with(
            ["arp", "-a", "192.168.1.10"], encoding="utf-8", errors="ignore"
        )

    @patch("app.services.arp.subprocess.check_output", side_effect=OSError)
    def test_get_mac_address_returns_unknown_when_arp_is_unavailable(self, _check_output):
        self.assertEqual(get_mac_address("192.168.1.10"), "Unknown")

    def test_oui_normalization_and_lookup(self):
        self.assertEqual(_normalize_oui_prefix("aabb.cc"), "AA:BB:CC")
        self.assertIsNone(_normalize_oui_prefix("not an oui"))
        self.assertEqual(get_manufacturer("aa-bb-cc-dd-ee-ff", {"AA:BB:CC": "Acme"}), "Acme")
        self.assertEqual(get_manufacturer("Unknown", {}), "Unknown")

    def test_load_oui_skips_invalid_rows(self):
        from tempfile import NamedTemporaryFile

        with NamedTemporaryFile(mode="w", encoding="utf-8", delete=False) as file:
            file.write("OUI,Manufacturer\nAA-BB-CC,Acme Networks\ninvalid,Bad\n")
            file_path = file.name
        try:
            self.assertEqual(load_oui(file_path), {"AA:BB:CC": "Acme Networks"})
        finally:
            import os
            os.unlink(file_path)

    @patch("app.services.ping.subprocess.run")
    @patch("app.services.ping.platform.system", return_value="Windows")
    def test_ping_host_returns_parsed_latency(self, _system, run):
        run.return_value = MagicMock(returncode=0, stdout="Reply from 10.0.0.1: time=2.5ms")
        self.assertEqual(ping_host("10.0.0.1", 500), (True, 2.5))

    @patch("app.services.ping.subprocess.run", side_effect=subprocess.TimeoutExpired("ping", 2))
    def test_ping_host_handles_command_timeout(self, _run):
        self.assertEqual(ping_host("10.0.0.1"), (False, None))

    @patch("app.services.ports.check_port")
    def test_scan_ports_returns_only_open_ports_in_numeric_order(self, check_port):
        check_port.side_effect = lambda _ip, port, _timeout: port in {443, 22}
        self.assertEqual(
            scan_ports("10.0.0.1", {443: "HTTPS", 22: "SSH", 80: "HTTP"}, max_workers=2),
            [{"port": 22, "service": "SSH"}, {"port": 443, "service": "HTTPS"}],
        )


class ScannerTests(unittest.TestCase):
    @patch("app.services.scanner.get_manufacturer", return_value="Acme")
    @patch("app.services.scanner.get_hostname", return_value="host")
    @patch("app.services.scanner.get_mac_address", return_value="AA:BB:CC:DD:EE:FF")
    @patch("app.services.scanner.ping_host", return_value=(False, None))
    def test_discover_host_keeps_device_with_arp_signal(self, *_mocks):
        device = NetworkScanner().discover_host("10.0.0.2")
        self.assertEqual(device["ip"], "10.0.0.2")
        self.assertEqual(device["manufacturer"], "Acme")

    @patch("app.services.scanner.get_mac_address", return_value="Unknown")
    @patch("app.services.scanner.ping_host", return_value=(False, None))
    def test_discover_host_discards_unreachable_device_without_mac(self, *_mocks):
        self.assertIsNone(NetworkScanner().discover_host("10.0.0.2"))

    def test_gateway_candidates_handle_small_networks(self):
        from ipaddress import ip_network

        self.assertFalse(_is_gateway_candidate("10.0.0.0", ip_network("10.0.0.0/31")))
        self.assertTrue(_is_gateway_candidate("10.0.0.1", ip_network("10.0.0.0/24")))
        self.assertTrue(_is_gateway_candidate("10.0.0.254", ip_network("10.0.0.0/24")))

