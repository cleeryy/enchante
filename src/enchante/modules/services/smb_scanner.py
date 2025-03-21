from ...core.scanner import Scanner


class SmbScanner(Scanner):
    """Scan SMB services for shares and vulnerabilities."""

    def __init__(self, target, options=None):
        super().__init__(target, options)
        self.port = self.options.get("port", 445)

    def scan(self):
        """Scan SMB service."""
        self.logger.info(f"Scanning SMB service on {self.target}:{self.port}")

        # Use nmap scripts for SMB scanning
        nmap_command = f"nmap -p{self.port} --script smb-enum-shares,smb-enum-users,smb-os-discovery {self.target}"

        if self.verbosity >= 2:
            nmap_command += ",smb-brute,smb-enum-domains,smb-protocols,smb-security-mode,smb-server-stats"

        if self.verbosity >= 3:
            nmap_command += ",smb-vuln-*"

        result = self.run_tool("nmap", nmap_command)

        if not result["success"]:
            self.logger.error(f"SMB scan failed: {result['stderr']}")
            self.results = {"status": "failed", "error": result["stderr"]}
            return self.results

        # Use enum4linux for additional enumeration
        enum4linux_command = f"enum4linux -a {self.target}"
        enum4linux_result = self.run_tool("enum4linux", enum4linux_command)

        self.results = {
            "status": "completed",
            "nmap_scan": result["stdout"],
            "enum4linux_scan": (
                enum4linux_result["stdout"] if enum4linux_result["success"] else None
            ),
        }

        return self.results
