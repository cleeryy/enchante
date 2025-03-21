import logging
import os
import subprocess
import sys
from typing import Dict, List


class ToolManager:
    """Manages external pentesting tools used by scanner modules."""

    COMMON_TOOLS = {
        "nmap": {
            "apt": "nmap",
            "check_command": "nmap --version",
        },
        "gobuster": {
            "apt": "gobuster",
            "check_command": "gobuster version",
        },
        "ffuf": {
            "apt": "ffuf",
            "check_command": "ffuf -V",
        },
        "nikto": {
            "apt": "nikto",
            "check_command": "nikto -Version",
        },
        "sqlmap": {
            "apt": "sqlmap",
            "check_command": "sqlmap --version",
        },
        "wpscan": {
            "apt": "wpscan",
            "check_command": "wpscan --version",
        },
        "hydra": {
            "apt": "hydra",
            "check_command": "hydra -h",
        },
        "enum4linux": {
            "apt": "enum4linux",
            "check_command": "enum4linux -h",
        },
    }

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.installed_tools = {}

    def is_tool_installed(self, tool_name: str) -> bool:
        """Check if a tool is installed and available in PATH."""
        if tool_name in self.installed_tools:
            return self.installed_tools[tool_name]

        tool_info = self.COMMON_TOOLS.get(tool_name)
        if not tool_info:
            self.logger.warning(f"Unknown tool: {tool_name}")
            return False

        try:
            subprocess.run(
                tool_info["check_command"].split(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
            self.installed_tools[tool_name] = True
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            self.installed_tools[tool_name] = False
            return False

    def install_tool(self, tool_name: str) -> bool:
        """Attempt to install a tool if it's not already installed."""
        if self.is_tool_installed(tool_name):
            self.logger.info(f"Tool {tool_name} is already installed.")
            return True

        tool_info = self.COMMON_TOOLS.get(tool_name)
        if not tool_info:
            self.logger.error(f"Unknown tool: {tool_name}")
            return False

        try:
            self.logger.info(f"Installing {tool_name}...")
            subprocess.run(
                ["apt", "update"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
            subprocess.run(
                ["apt", "install", "-y", tool_info["apt"]],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )

            if self.is_tool_installed(tool_name):
                self.logger.info(f"Successfully installed {tool_name}")
                return True
            else:
                self.logger.error(f"Failed to install {tool_name}")
                return False
        except subprocess.SubprocessError as e:
            self.logger.error(f"Error installing {tool_name}: {str(e)}")
            return False

    def ensure_tool_available(self, tool_name: str) -> bool:
        """Check if a tool is installed, and install it if needed."""
        if self.is_tool_installed(tool_name):
            return True

        return self.install_tool(tool_name)

    def get_available_tools(self) -> List[str]:
        """Return a list of available tools."""
        available_tools = []
        for tool_name in self.COMMON_TOOLS:
            if self.is_tool_installed(tool_name):
                available_tools.append(tool_name)
        return available_tools
