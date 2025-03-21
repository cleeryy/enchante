from ...core.scanner import Scanner


class PortScanner(Scanner):
    """Scan for open ports on a target using nmap."""

    def __init__(self, target, options=None):
        super().__init__(target, options)
        self.ports = self.options.get("ports", "1-1000")
        self.scan_type = self.options.get(
            "scan_type", "SV"
        )  # Default to service version detection

    def scan(self):
        """Scan ports using nmap."""
        self.logger.info(f"Scanning ports {self.ports} on {self.target}")

        # Build nmap command based on verbosity
        nmap_command = f"nmap -p{self.ports} -T4 -{self.scan_type}"

        # Add verbosity flags based on our verbosity level
        if self.verbosity >= 2:
            nmap_command += " -v"
        if self.verbosity >= 3:
            nmap_command += "v"

        nmap_command += f" {self.target}"

        result = self.run_tool("nmap", nmap_command)

        if not result["success"]:
            self.logger.error(f"Nmap scan failed: {result['stderr']}")
            self.results = {"status": "failed", "error": result["stderr"]}
            return self.results

        # Parse nmap output for open ports
        open_ports = []
        for line in result["stdout"].splitlines():
            if "/tcp" in line and "open" in line:
                parts = line.strip().split()
                if len(parts) >= 2:
                    port = parts[0].split("/")[0]
                    service = parts[2] if len(parts) > 2 else "unknown"
                    open_ports.append({"port": port, "service": service})

        self.results = {
            "status": "completed",
            "open_ports": open_ports,
            "raw_output": result["stdout"] if self.verbosity >= 2 else None,
        }

        return self.results
