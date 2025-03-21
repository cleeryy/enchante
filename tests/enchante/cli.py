import json
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from enchante.core.logger import get_logger
from enchante.core.module import ModuleManager

app = typer.Typer(help="Enchante - A Modular Penetration Testing Framework")
console = Console()


def setup(verbosity: int = 0):
    """Initial setup to discover modules."""
    # Configure root logger
    logger = get_logger("enchante", verbosity)
    return ModuleManager(verbosity)


@app.command()
def list_modules(
    verbose: Optional[int] = typer.Option(
        0, "--verbose", "-v", count=True, help="Increase verbosity"
    )
):
    """List all available modules."""
    module_manager = setup(verbose)
    module_manager.discover_modules()
    modules = module_manager.get_available_modules()

    if not modules:
        console.print(
            "[yellow]No modules found. Make sure the modules directory exists.[/yellow]"
        )
        return

    table = Table(title="Available Modules")
    table.add_column("Module Name", style="cyan")

    for module in sorted(modules):
        table.add_row(module)

    console.print(table)


@app.command()
def list_tools(
    verbose: Optional[int] = typer.Option(
        0, "--verbose", "-v", count=True, help="Increase verbosity"
    )
):
    """List all available external tools."""
    setup(verbose)
    from enchante.core.tools import ToolManager

    tool_manager = ToolManager()
    available_tools = tool_manager.get_available_tools()
    missing_tools = [
        tool for tool in tool_manager.COMMON_TOOLS if tool not in available_tools
    ]

    table = Table(title="External Tools Status")
    table.add_column("Tool Name", style="cyan")
    table.add_column("Status", style="green")

    for tool in sorted(tool_manager.COMMON_TOOLS.keys()):
        status = "[green]Available" if tool in available_tools else "[red]Not Installed"
        table.add_row(tool, status)

    console.print(table)

    if missing_tools:
        console.print("\n[yellow]To install missing tools, run with sudo:[/yellow]")
        console.print("sudo enchante install-tools")


@app.command()
def install_tools(
    tool: Optional[str] = typer.Option(
        None, "--tool", "-t", help="Specific tool to install"
    ),
    verbose: Optional[int] = typer.Option(
        0, "--verbose", "-v", count=True, help="Increase verbosity"
    ),
):
    """Install missing external tools."""
    logger = get_logger("enchante.install", verbose)
    from enchante.core.tools import ToolManager

    tool_manager = ToolManager(logger)

    if tool:
        if tool not in tool_manager.COMMON_TOOLS:
            console.print(f"[bold red]Unknown tool: {tool}[/bold red]")
            return

        if tool_manager.is_tool_installed(tool):
            console.print(f"[green]Tool {tool} is already installed[/green]")
        else:
            console.print(f"Installing {tool}...")
            success = tool_manager.install_tool(tool)
            if success:
                console.print(f"[green]Successfully installed {tool}[/green]")
            else:
                console.print(f"[bold red]Failed to install {tool}[/bold red]")
    else:
        # Install all missing tools
        missing_tools = [
            tool
            for tool in tool_manager.COMMON_TOOLS
            if not tool_manager.is_tool_installed(tool)
        ]

        if not missing_tools:
            console.print("[green]All tools are already installed[/green]")
            return

        for tool in missing_tools:
            console.print(f"Installing {tool}...")
            success = tool_manager.install_tool(tool)
            if success:
                console.print(f"[green]Successfully installed {tool}[/green]")
            else:
                console.print(f"[bold red]Failed to install {tool}[/bold red]")


@app.command()
def scan(
    target: str = typer.Argument(..., help="Target to scan (IP, hostname, or URL)"),
    module: str = typer.Option(None, "--module", "-m", help="Specific module to run"),
    output: Optional[str] = typer.Option(
        None, "--output", "-o", help="Output file for results (JSON format)"
    ),
    verbose: Optional[int] = typer.Option(
        0, "--verbose", "-v", count=True, help="Increase verbosity"
    ),
):
    """Scan a target using the specified module or all modules."""
    module_manager = setup(verbose)
    logger = get_logger("enchante.scan", verbose)

    logger.info(f"Starting scan of {target} with verbosity level {verbose}")
    module_manager.discover_modules()

    modules = module_manager.get_available_modules()

    if not modules:
        console.print("[bold red]No modules found. Aborting.[/bold red]")
        return

    results = {}
    options = {"verbosity": verbose}

    if module:
        # Run a specific module
        if module not in modules:
            console.print(f"[bold red]Module '{module}' not found.[/bold red]")
            return

        with console.status(f"Running module {module} on {target}..."):
            try:
                logger.info(f"Running module: {module}")
                module_result = module_manager.run_module(module, target, options)
                results[module] = module_result
            except Exception as e:
                logger.error(f"Error running module {module}: {str(e)}")
                results[module] = {"error": str(e)}
    else:
        # Run all modules
        with console.status(f"Running all modules on {target}..."):
            for mod in modules:
                try:
                    logger.info(f"Running module: {mod}")
                    if verbose >= 1:
                        console.print(f"Running module: {mod}")
                    module_result = module_manager.run_module(mod, target, options)
                    results[mod] = module_result
                except Exception as e:
                    logger.error(f"Error running module {mod}: {str(e)}")
                    results[mod] = {"error": str(e)}

    # Display results based on verbosity
    if verbose >= 1:
        for mod_name, mod_results in results.items():
            console.print(f"\n[bold cyan]Results from {mod_name}:[/bold cyan]")
            console.print(mod_results)
    else:
        # Simplified output for default verbosity
        console.print("\n[bold cyan]Scan Results Summary:[/bold cyan]")
        table = Table(title=f"Scan Results for {target}")
        table.add_column("Module", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Findings", style="yellow")

        for mod_name, mod_results in results.items():
            status = mod_results.get("status", "unknown")
            if "error" in mod_results:
                status = "failed"
                findings = mod_results["error"]
            else:
                findings = "See detailed output (-v)"

            table.add_row(mod_name, status, findings)

        console.print(table)

    # Save results to file if requested
    if output:
        with open(output, "w") as f:
            json.dump(results, f, indent=4)
        console.print(f"\n[green]Results saved to {output}[/green]")


if __name__ == "__main__":
    app()
