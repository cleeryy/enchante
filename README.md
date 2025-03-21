# Enchante

Enchante is a comprehensive modular penetration testing framework designed for CTF competitions and security assessments. The name comes from the French word "enchanté" (meaning "enchanted" or "pleased to meet you"), reflecting the framework's elegant approach to security testing.

![Enchante Logo](https://placehold.co/800x200?text=Enchante)

- **Modular Architecture**: Easily extend with custom modules
- **Tool Integration**: Seamless integration with popular security tools (nmap, gobuster, nikto, etc.)
- **Multiple Verbosity Levels**: Control the amount of information displayed
- **Automatic Tool Management**: Detects and installs missing dependencies
- **Easy-to-Use CLI**: Simple command-line interface with intuitive commands
- **Comprehensive Logging**: Detailed logs for all operations
- **Flexible Output Formats**: Save results in structured formats for further analysis

## Installation

### Prerequisites

- Python 3.6+
- Pip package manager
- Sudo privileges (for tool installation)

### Installation Steps

```bash
# Clone the repository
git clone https://github.com/yourusername/enchante.git
cd enchante

# Install the package in development mode
pip install -e .

# Check if external tools are installed
enchante list-tools

# Install missing tools (if needed)
sudo enchante install-tools
```

## Usage

### Basic Commands

```bash
# List all available modules
enchante list-modules

# Check the status of external tools
enchante list-tools

# Install missing external tools
sudo enchante install-tools

# Perform a basic scan
enchante scan target.example.com

# Scan a specific target with a specific module
enchante scan target.example.com --module port_scanner.PortScanner

# Save scan results to a file
enchante scan target.example.com --output results.json
```

### Verbosity Levels

Enchante supports multiple verbosity levels to control the amount of information displayed:

```bash
# Default verbosity (only warnings and errors)
enchante scan target.example.com

# Level 1: Informational messages (-v)
enchante scan target.example.com -v

# Level 2: Verbose details (-vv)
enchante scan target.example.com -vv

# Level 3: Debug information (-vvv)
enchante scan target.example.com -vvv
```

## Modules

Enchante comes with several built-in modules organized by category:

### Network Modules

- **Port Scanner**: Scans for open ports using nmap

### Web Modules

- **Directory Scanner**: Discovers directories and files using gobuster or ffuf
- **Nikto Scanner**: Scans web servers for vulnerabilities

### Service Modules

- **SSH Scanner**: Analyzes SSH services for vulnerabilities
- **SMB Scanner**: Enumerates SMB shares and checks for vulnerabilities

## Creating Custom Modules

Enchante's modular architecture makes it easy to create and integrate your own scanning modules.

### Module Structure

Create a new Python file in the appropriate subdirectory of `enchante/modules/`:

```python
from ...core.scanner import Scanner

class CustomScanner(Scanner):
    """Description of your custom scanner."""

    def __init__(self, target, options=None):
        super().__init__(target, options)
        # Initialize any module-specific options
        self.custom_option = self.options.get("custom_option", "default_value")

    def scan(self):
        """Execute the scan."""
        self.logger.info(f"Scanning {self.target} with {self.__class__.__name__}")

        # Your scanning logic here
        # You can use self.run_tool() to execute external tools

        # Example:
        result = self.run_tool("some_tool", f"some_tool --arg1 {self.target}")

        self.results = {
            'status': 'completed',
            'findings': ["Finding 1", "Finding 2"],
            'raw_output': result['stdout'] if self.verbosity >= 2 else None
        }

        return self.results
```

### Module Discovery

Modules are automatically discovered when you run Enchante. The framework searches through all directories in the `enchante/modules/` package and registers any classes that inherit from the `Scanner` base class.

## External Tool Integration

Enchante can use the following external tools:

| Tool       | Purpose                             |
| ---------- | ----------------------------------- |
| nmap       | Port scanning and service detection |
| gobuster   | Web directory enumeration           |
| ffuf       | Web content discovery               |
| nikto      | Web server vulnerability scanning   |
| sqlmap     | SQL injection testing               |
| wpscan     | WordPress vulnerability scanning    |
| hydra      | Password brute forcing              |
| enum4linux | Windows/Samba enumeration           |

The tool manager will automatically check if these tools are installed and can install them if needed.

## Example Workflows

### Basic Network Reconnaissance

```bash
# Perform a comprehensive scan of a target
enchante scan target.example.com -v --output recon.json
```

### Web Application Testing

```bash
# Focus on web application testing
enchante scan https://target.example.com --module web.DirectoryScanner -vv
enchante scan https://target.example.com --module web.NiktoScanner -v
```

### Service-Specific Assessment

```bash
# Assess SSH security
enchante scan target.example.com --module service.SSHScanner -vv

# Enumerate SMB shares
enchante scan target.example.com --module service.SmbScanner -v
```

## Example Output

```
Enchante - A Modular Penetration Testing Framework

Starting scan of example.com with verbosity level 1
Running module: port_scanner.PortScanner
Running module: web.DirectoryScanner
Running module: web.NiktoScanner
Running module: service.SSHScanner
Running module: service.SmbScanner

Scan Results Summary:
┏━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Module                 ┃ Status    ┃ Findings                    ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ port_scanner.PortScanner │ completed │ 3 open ports found         │
│ web.DirectoryScanner   │ completed │ 12 directories discovered   │
│ web.NiktoScanner       │ completed │ 5 vulnerabilities detected  │
│ service.SSHScanner     │ completed │ SSH v2.0 detected           │
│ service.SmbScanner     │ failed    │ Service not available       │
└────────────────────────┴───────────┴─────────────────────────────┘

Results saved to results.json
```

## Project Structure

```
enchante/
├── enchante/
│   ├── __init__.py
│   ├── cli.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   ├── module.py
│   │   ├── scanner.py
│   │   └── tools.py
│   └── modules/
│       ├── __init__.py
│       ├── network/
│       │   ├── __init__.py
│       │   └── port_scanner.py
│       ├── service/
│       │   ├── __init__.py
│       │   ├── smb_scanner.py
│       │   └── ssh_scanner.py
│       └── web/
│           ├── __init__.py
│           ├── directory_scanner.py
│           └── nikto_scanner.py
├── setup.py
└── README.md
```

## Contributing

Contributions are welcome! Here's how you can contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Create new modules in the appropriate directories
5. Test your changes thoroughly
6. Commit your changes (`git commit -m 'Add some amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Thanks to all the open-source security tools that Enchante integrates with
- Special thanks to the Python community for providing the libraries that make this project possible

---

Created with ❤️ for the security community and CTF enthusiasts

---
