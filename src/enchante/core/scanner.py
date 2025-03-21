import logging
import subprocess
from abc import ABC, abstractmethod
from typing import Any, Dict

from .tools import ToolManager


class Scanner(ABC):
    """Base scanner class that all scanning modules will inherit from."""

    def __init__(self, target, options=None):
        self.target = target
        self.options = options or {}
        self.results = {}
        self.verbosity = self.options.get("verbosity", 0)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.tool_manager = ToolManager(self.logger)

    @abstractmethod
    def scan(self):
        """Execute the scan. Must be implemented by subclasses."""
        pass

    def get_results(self):
        """Return the scan results."""
        return self.results

    def run_tool(self, tool_name: str, command: str) -> Dict[str, Any]:
        """Run an external tool and capture its output."""
        if not self.tool_manager.ensure_tool_available(tool_name):
            self.logger.error(
                f"Tool {tool_name} is not available and could not be installed."
            )
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Tool {tool_name} is not available",
                "command": command,
            }

        try:
            self.logger.info(f"Running command: {command}")
            process = subprocess.run(
                command.split(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            if self.verbosity >= 2:  # Show detailed output for -vv and above
                self.logger.verbose(f"Command output:\n{process.stdout}")
                if process.stderr:
                    self.logger.verbose(f"Command errors:\n{process.stderr}")

            return {
                "success": process.returncode == 0,
                "stdout": process.stdout,
                "stderr": process.stderr,
                "command": command,
            }
        except Exception as e:
            self.logger.error(f"Error running {tool_name}: {str(e)}")
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "command": command,
            }
