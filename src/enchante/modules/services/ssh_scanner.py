from ...core.scanner import Scanner


class SSHScanner(Scanner):
    """Scan SSH services for vulnerabilities and attempt basic enumeration."""

    def __init__(self, target, options=None):
        super().__init__(target, options)
        self.port = self.options.get("port", 22)
        self.usernames = self.options.get("usernames", ["root", "admin", "user"])
        self.passwords = self.options.get("passwords", ["password", "admin", "123456"])

    def scan(self):
        """Scan SSH service for vulnerabilities and attempt login."""
        self.logger.info(f"Scanning SSH service on {self.target}:{self.port}")

        # First use nmap for SSH scanning
        nmap_command = f"nmap -p{self.port} --script ssh-auth-methods,ssh-hostkey,ssh-brute -T4 {self.target}"

        result = self.run_tool("nmap", nmap_command)

        if not result["success"]:
            self.logger.error(f"SSH scan failed: {result['stderr']}")
            self.results = {"status": "failed", "error": result["stderr"]}
            return self.results

        # Try hydra for brute force if we have enough verbosity level
        hydra_results = None
        if self.verbosity >= 2:
            # Create temporary username and password files
            import os
            import tempfile

            with tempfile.NamedTemporaryFile(mode="w", delete=False) as user_file:
                for user in self.usernames:
                    user_file.write(f"{user}\n")
                user_file_path = user_file.name

            with tempfile.NamedTemporaryFile(mode="w", delete=False) as pass_file:
                for password in self.passwords:
                    pass_file.write(f"{password}\n")
                pass_file_path = pass_file.name

            try:
                hydra_command = f"hydra -L {user_file_path} -P {pass_file_path} -t 4 ssh://{self.target}:{self.port}"
                hydra_results = self.run_tool("hydra", hydra_command)
            finally:
                # Clean up temp files
                os.unlink(user_file_path)
                os.unlink(pass_file_path)

        self.results = {
            "status": "completed",
            "nmap_scan": result["stdout"],
            "hydra_scan": (
                hydra_results["stdout"]
                if hydra_results and hydra_results["success"]
                else None
            ),
        }

        return self.results
