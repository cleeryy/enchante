from ...core.scanner import Scanner


class NiktoScanner(Scanner):
    """Scan web server for vulnerabilities using Nikto."""

    def __init__(self, target, options=None):
        super().__init__(target, options)
        self.port = self.options.get("port", 80)

        # Ensure target URL has the correct format
        if self.target.startswith(("http://", "https://")):
            # Extract domain from URL
            from urllib.parse import urlparse

            parsed = urlparse(self.target)
            self.target = parsed.netloc
            if parsed.scheme == "https":
                self.port = 443

    def scan(self):
        """Scan web server using Nikto."""
        self.logger.info(f"Scanning web server {self.target}:{self.port} with Nikto")

        nikto_command = f"nikto -h {self.target} -p {self.port}"

        # Add verbosity flags based on our verbosity level
        if self.verbosity >= 1:
            nikto_command += " -Display V"  # Verbose output
        if self.verbosity >= 2:
            nikto_command += " -Display P"  # Show progress
        if self.verbosity >= 3:
            nikto_command += " -Debug"  # Debug level

        result = self.run_tool("nikto", nikto_command)

        if not result["success"]:
            self.logger.error(f"Nikto scan failed: {result['stderr']}")
            self.results = {"status": "failed", "error": result["stderr"]}
            return self.results

        self.results = {
            "status": "completed",
            "raw_output": result["stdout"],
            "command": result["command"],
        }

        return self.results
