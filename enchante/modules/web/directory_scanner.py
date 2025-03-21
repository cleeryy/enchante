from ...core.scanner import Scanner


class DirectoryScanner(Scanner):
    """Scan for directories and files on a web server using gobuster or ffuf."""

    def __init__(self, target, options=None):
        super().__init__(target, options)
        self.wordlist = self.options.get(
            "wordlist", "/usr/share/wordlists/dirb/common.txt"
        )
        self.extensions = self.options.get("extensions", "php,html,txt")
        self.threads = self.options.get("threads", 10)
        self.tool = self.options.get("tool", "gobuster")  # gobuster or ffuf

        # Ensure target URL has the correct format
        if not self.target.startswith(("http://", "https://")):
            self.target = f"http://{self.target}"

    def scan(self):
        """Scan for directories using the selected tool."""
        self.logger.info(f"Scanning directories on {self.target} using {self.tool}")

        # Try to use selected tool, fall back to other if not available
        if self.tool == "gobuster" and not self.tool_manager.is_tool_installed(
            "gobuster"
        ):
            if self.tool_manager.is_tool_installed("ffuf"):
                self.logger.warning("Gobuster not found, falling back to ffuf")
                self.tool = "ffuf"

        if self.tool == "ffuf" and not self.tool_manager.is_tool_installed("ffuf"):
            if self.tool_manager.is_tool_installed("gobuster"):
                self.logger.warning("Ffuf not found, falling back to gobuster")
                self.tool = "gobuster"

        if self.tool == "gobuster":
            command = f"gobuster dir -u {self.target} -w {self.wordlist} -x {self.extensions} -t {self.threads}"
            if self.verbosity >= 2:
                command += " -v"
        else:  # ffuf
            command = f"ffuf -u {self.target}/FUZZ -w {self.wordlist}:FUZZ -e .{self.extensions.replace(',', ',.') if self.extensions else ''} -t {self.threads}"
            if self.verbosity >= 2:
                command += " -v"

        result = self.run_tool(self.tool, command)

        if not result["success"]:
            self.logger.error(f"{self.tool} scan failed: {result['stderr']}")
            self.results = {"status": "failed", "error": result["stderr"]}
            return self.results

        self.results = {
            "status": "completed",
            "raw_output": result["stdout"],
            "command": result["command"],
        }

        return self.results
