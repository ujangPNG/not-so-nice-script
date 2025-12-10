# VPN Gate Crawler

A Python-based tool to automatically download OpenVPN configuration files from VPN Gate and import them into NetworkManager.

## Description

This project consists of two Python scripts that work together to:
1. Crawl the VPN Gate website and download available OpenVPN configuration files
2. Import the downloaded configurations into NetworkManager for easy VPN connection management

VPN Gate is a free VPN service provided by volunteers around the world. This tool automates the process of downloading and configuring VPN connections from their service.

## Features

- **Automatic Crawling**: Scans VPN Gate website for available VPN servers
- **Bulk Download**: Downloads multiple OpenVPN configuration files at once
- **Smart Filtering**: Avoids downloading duplicate configurations
- **NetworkManager Integration**: Automatically imports configurations into NetworkManager
- **Error Handling**: Gracefully handles network errors and duplicate entries

## Prerequisites

- Python 3.x
- NetworkManager (for importing VPN configurations)
- `nmcli` command-line tool (typically included with NetworkManager)
- Linux-based operating system (for NetworkManager support)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/ujangPNG/not-so-nice-script.git
cd not-so-nice-script
```

2. Ensure Python 3 is installed:
```bash
python3 --version
```

3. Make the scripts executable (optional):
```bash
chmod +x vpngate_crawler.py import_vpn_configs.py
```

## Usage

### Step 1: Download VPN Configurations

Run the crawler script to download OpenVPN configuration files:

```bash
python3 vpngate_crawler.py
```

This will:
- Create an `openvpnfile` directory if it doesn't exist
- Crawl the VPN Gate website
- Download available `.ovpn` configuration files
- Save them to the `openvpnfile` directory

### Step 2: Import to NetworkManager

After downloading the configurations, import them into NetworkManager:

```bash
sudo python3 import_vpn_configs.py
```

**Note**: This script requires sudo privileges to modify NetworkManager connections.

This will:
- Scan the `openvpnfile` directory for `.ovpn` files
- Import each configuration into NetworkManager
- Skip configurations that already exist
- Report success/failure statistics

### Connecting to a VPN

After importing, you can connect to any VPN through:
- NetworkManager GUI (system tray icon)
- Command line: `nmcli connection up <connection-name>`

## Project Structure

```
.
├── vpngate_crawler.py      # Main crawler script to download VPN configs
├── import_vpn_configs.py   # Script to import configs into NetworkManager
└── openvpnfile/            # Directory where .ovpn files are stored (created automatically)
```

## Important Notes

- **Legal Disclaimer**: Ensure you comply with VPN Gate's terms of service and your local laws regarding VPN usage
- **Security**: VPN Gate servers are run by volunteers. Use at your own discretion and risk
- **Privacy**: While VPNs can enhance privacy, free VPN services may have limitations
- **Connection Quality**: VPN server availability and speed may vary
- **Sudo Requirements**: The import script requires root privileges to modify NetworkManager settings

## Troubleshooting

**No .ovpn files downloaded:**
- Check your internet connection
- VPN Gate website might be temporarily unavailable
- Try running the crawler script again

**Import fails:**
- Ensure NetworkManager is installed and running
- Verify you're running the import script with sudo
- Check that the `openvpnfile` directory contains `.ovpn` files

**Can't connect to VPN:**
- Some VPN servers may be offline or overloaded
- Try a different VPN configuration
- Check NetworkManager logs: `journalctl -u NetworkManager`

## License

This project is provided as-is for educational and personal use. Please respect VPN Gate's terms of service and use responsibly.

## Contributing

Feel free to submit issues or pull requests if you have suggestions for improvements.

## Acknowledgments

- [VPN Gate](https://www.vpngate.net/) for providing free VPN services
- All volunteer VPN server operators
