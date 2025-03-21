import importlib
import inspect
import logging
import pkgutil
from typing import Dict, List, Optional, Type

from .logger import get_logger
from .scanner import Scanner


class ModuleManager:
    """Manages loading and running scanner modules."""

    def __init__(self, verbosity: int = 0):
        self.modules: Dict[str, Type[Scanner]] = {}
        self.verbosity = verbosity
        self.logger = get_logger("enchante.modules", verbosity)

    def discover_modules(self, package_name: str = "enchante.modules"):
        """Discover and load all available scanner modules."""
        self.logger.info(f"Discovering modules in {package_name}")

        try:
            package = importlib.import_module(package_name)

            for _, name, is_pkg in pkgutil.iter_modules(
                package.__path__, package.__name__ + "."
            ):
                if is_pkg:
                    # Recursively discover modules in subpackages
                    self.discover_modules(name)
                else:
                    try:
                        module = importlib.import_module(name)
                        self._register_scanners_from_module(module)
                    except Exception as e:
                        self.logger.error(f"Error loading module {name}: {str(e)}")
        except ImportError as e:
            self.logger.error(f"Error importing package {package_name}: {str(e)}")

    def _register_scanners_from_module(self, module):
        """Register all Scanner classes from the given module."""
        for name, obj in inspect.getmembers(module):
            if (
                inspect.isclass(obj)
                and issubclass(obj, Scanner)
                and obj != Scanner
                and obj.__module__ == module.__name__
            ):

                module_name = obj.__module__.split(".")[-1]
                key = f"{module_name}.{name}"
                self.modules[key] = obj
                self.logger.verbose(f"Registered scanner: {key}")

    def get_available_modules(self) -> List[str]:
        """Return a list of all available module names."""
        return list(self.modules.keys())

    def get_module(self, module_name: str) -> Type[Scanner]:
        """Get a module class by name."""
        if module_name not in self.modules:
            raise ValueError(f"Module {module_name} not found")
        return self.modules[module_name]

    def run_module(
        self, module_name: str, target: str, options: Optional[dict] = None
    ) -> dict:
        """Run a module by name and return its results."""
        options = options or {}

        # Ensure verbosity is set in options
        if "verbosity" not in options:
            options["verbosity"] = self.verbosity

        self.logger.info(f"Running module {module_name} on target {target}")

        module_class = self.get_module(module_name)
        scanner = module_class(target, options)

        try:
            scanner.scan()
            results = scanner.get_results()
            return results
        except Exception as e:
            self.logger.error(f"Error in module {module_name}: {str(e)}")
            return {"status": "error", "error": str(e)}
