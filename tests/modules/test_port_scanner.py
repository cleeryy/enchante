import pytest

from enchante.modules.network.port_scanner import PortScanner


def test_port_scanner_initialization():
    """Test that the PortScanner initializes correctly"""
    scanner = PortScanner("example.com", {"ports": "80,443"})
    assert scanner.target == "example.com"
    assert scanner.ports == "80,443"


# Mock the run_tool method to avoid actual network calls during testing
@pytest.fixture
def mock_port_scanner(monkeypatch):
    def mock_run_tool(self, tool_name, command):
        return {
            "success": True,
            "stdout": "80/tcp open  http\n443/tcp open  https",
            "stderr": "",
            "command": command,
        }

    monkeypatch.setattr(PortScanner, "run_tool", mock_run_tool)
    return PortScanner("example.com")


def test_port_scanner_scan(mock_port_scanner):
    """Test that scan method correctly parses nmap output"""
    result = mock_port_scanner.scan()
    assert result["status"] == "completed"
    assert len(result["open_ports"]) == 2
