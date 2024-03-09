# EthOrb Installation Guide

Welcome to the EthOrb Installation Guide. This guide will walk you through the process of installing and setting up the EthOrb package for interacting with Ethereum blockchain networks.

## Prerequisites

Before you begin, ensure you have the following prerequisites installed on your system:

- Python 3.x
- pip (Python package manager)

## Installation Methods

### 1. Install from PyPI (Recommended)

You can install EthOrb using pip, the Python package manager. Open your terminal or command prompt and run the following command:

```bash
$ pip install ethorb
```

This command will download and install the latest version of EthOrb from the Python Package Index (PyPI).

### 2. Install from Source

Alternatively, you can install EthOrb from the source code repository. First, clone the repository to your local machine:

```bash
$ git clone https://github.com/ethorb/ethorb.git
```

Then, navigate to the project directory and install EthOrb using pip:

```bash
$ cd ethorb
$ pip install .
```

This command will install EthOrb using the source files in the current directory.

## Configuration

Once EthOrb is installed, you need to configure it with your Ethereum network URL. You can do this by creating an instance of the `Blockchain` class with your network URL. Here's an example:

```python
from ethorb import Blockchain

# Initialize a new instance of Blockchain with your network URL
eth = Blockchain("https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID")
```

Replace `"https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"` with your actual Ethereum network URL.

## Usage

Now that EthOrb is installed and configured, you can start using it to interact with Ethereum blockchain networks. Refer to the [Usage Guide](usage.md) for detailed documentation on the available classes, methods, and functions.

## Support

If you have any further questions or need assistance, please don't hesitate to inform. You can always join EthOrb's GitHub Discussion.

---

This concludes the EthOrb Installation Guide. Happy blockchain development!
