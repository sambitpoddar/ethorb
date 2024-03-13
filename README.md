[![Last commit](https://img.shields.io/github/last-commit/sambitpoddar/ethorb)](https://github.com/sambitpoddar/ethorb/commits/main)
[![Code Size](https://img.shields.io/github/languages/code-size/sambitpoddar/ethorb)](https://github.com/sambitpoddar/ethorb)
[![Python3.11](https://img.shields.io/badge/Python-3.11-green.svg?style=flat-square)](https://www.python.org/downloads/release/python-2714/)
[![PyPI version](https://badge.fury.io/py/your-package-name.svg)](https://badge.fury.io/py/your-package-name)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
<center><img src="assets/ethorblogo.png" alt="EthOrb Logo" width="300"/></center>

# EthOrb: A powerful toolkit for seamless interaction with Ethereum blockchain networks.

Welcome to EthOrb, a powerful Python package for interacting with Ethereum blockchain networks.

## Overview

EthOrb provides a comprehensive set of tools and utilities for developers to seamlessly integrate Ethereum blockchain functionality into their Python applications. Whether you're building decentralized applications (dApps), smart contracts, or simply need to interact with Ethereum networks programmatically, EthOrb offers a user-friendly and efficient solution.

## Key Features

- **Simple Integration:** EthOrb's intuitive interface makes it easy to incorporate Ethereum functionality into your Python projects.
- **Full Blockchain Support:** Access and interact with Ethereum mainnet, testnets (Ropsten, Rinkeby, Kovan), and private Ethereum networks.
- **Smart Contract Interaction:** Deploy, call, and interact with smart contracts directly from your Python code.
- **Transaction Management:** Send and receive transactions, estimate gas costs, and retrieve transaction receipts effortlessly.
- **Account Management:** Manage Ethereum accounts, including generating, importing, and exporting account keys securely.
- **Comprehensive Documentation:** Extensive documentation and examples to help you get started quickly and understand EthOrb's capabilities fully.

## Installation

You can install EthOrb via pip:

```bash
$ pip install ethorb
```

For more detailed installation instructions and requirements, please refer to the [Installation Guide](docs/installation.md) section in the documentation.

## Quick Start

To begin using EthOrb, follow these simple steps:

1. Install EthOrb using pip as shown in the Installation section.
2. Import EthOrb into your Python project:

```python
import ethorb
```

3. Initialize the EthOrb Blockchain-client with your preferred Ethereum network:

```python
from ethorb import Blockchain

# Connect to Ethereum network.
eth_orb = Blockchain(network_url="https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID")

```

This URL could be for mainnet, testnets like ropsten or rinkeby, or any custom network URL.


4. Start interacting with Ethereum blockchain networks seamlessly:

```python
# Get account balance
balance = eth_orb.get_balance(address="0x...")
print("Account balance:", balance)
```

For more detailed usage instructions and examples, please refer to the [Usage Guide](docs/usage.md) section in the documentation.

## Documentation

For comprehensive documentation, including installation instructions, usage guides, and more, please visit the [EthOrb Documentation](docs/readme.md).

## Author

- Sambit Poddar
  - Email: sambitpoddar@yahoo.com
  - LinkedIn: [LinkedIn](https://www.linkedin.com/in/sambitpoddar)

## Contributing

We welcome contributions from the community to improve EthOrb! Whether it's reporting bugs, suggesting new features, or submitting pull requests, your contributions are highly appreciated. Please refer to the [Contributing Guidelines](CONTRIBUTING.md) for more information.

## Support

If you encounter any issues or have any questions about EthOrb, please don't hesitate to [open an issue](https://github.com/sambitpoddar/ethorb/issues) on GitHub. Our community is here to help you resolve any problems and provide support as needed.

## License

EthOrb is licensed under the [Apache 2.0 License](LICENSE). Feel free to use, modify, and distribute EthOrb for both personal and commercial purposes. We only ask that you include the appropriate attribution and disclaimer notices in your projects.

---

Thank you for choosing EthOrb! We hope you find it helpful and look forward to seeing the amazing applications you build with it. Happy coding! 🚀🌐
