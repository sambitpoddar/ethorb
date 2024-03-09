# Usage Guide

Welcome to the EthOrb Usage Guide. This section provides detailed documentation for the classes, methods, and functions available in the EthOrb package for interacting with Ethereum blockchain networks.

## `Blockchain` Class

The `Blockchain` class is the main entry point for interacting with Ethereum blockchain networks. It provides various methods for managing wallets, sending transactions, deploying smart contracts, and more.

### Constructor

#### `__init__(network_url: str) -> None`

Initialize a new `Blockchain` instance with the specified Ethereum network URL.

- `network_url` (str): The URL of the Ethereum network to connect to.

### Wallet Management

#### `generate_wallet() -> Dict[str, str]`

Generate a new wallet address and private key.

- Returns:
  - `Dict[str, str]`: A dictionary containing the new wallet address and private key.

#### `get_balance(address: str) -> float`

Get the balance of a wallet address.

- `address` (str): The Ethereum address to get the balance for.
- Returns:
  - `float`: The balance of the address in Ether.

### Transaction Management

#### `send_transaction(sender_address: str, recipient_address: str, amount: float, private_key: str, gas_limit: int = None, gas_price: int = None, data: bytes = None, nonce: int = None, chain_id: int = None) -> str`

Send cryptocurrency from one address to another.

- `sender_address` (str): The sender's Ethereum address.
- `recipient_address` (str): The recipient's Ethereum address.
- `amount` (float): The amount of cryptocurrency to send, in Ether.
- `private_key` (str): The private key of the sender's Ethereum address.
- `gas_limit` (int, optional): The gas limit for the transaction.
- `gas_price` (int, optional): The gas price for the transaction.
- `data` (bytes, optional): Additional data to include in the transaction.
- `nonce` (int, optional): The nonce for the transaction.
- `chain_id` (int, optional): The chain ID for the transaction.
- Returns:
  - `str`: The transaction hash of the sent transaction.

### Smart Contract Deployment and Interaction

#### `deploy_contract(contract_code: Dict[str, Any], sender_address: str, private_key: str, gas_limit: int = None, gas_price: int = None, nonce: int = None, chain_id: int = None) -> str`

Deploy a smart contract to the blockchain.

- `contract_code` (Dict[str, Any]): The bytecode and ABI of the smart contract.
- `sender_address` (str): The address deploying the contract.
- `private_key` (str): The private key of the sender's Ethereum address.
- `gas_limit` (int, optional): The gas limit for the transaction.
- `gas_price` (int, optional): The gas price for the transaction.
- `nonce` (int, optional): The nonce for the transaction.
- `chain_id` (int, optional): The chain ID for the transaction.
- Returns:
  - `str`: The transaction hash of the contract deployment transaction.

#### `call_contract_function(contract_address: str, function_name: str, *args) -> Any`

Call a function of a smart contract.

- `contract_address` (str): The address of the smart contract.
- `function_name` (str): The name of the function to call.
- `*args`: Arguments to pass to the function.
- Returns:
  - `Any`: The result of the function call.

#### `listen_for_events(contract_address: str, event_name: str) -> List[Dict[str, Any]]`

Listen for events emitted by a smart contract.

- `contract_address` (str): The address of the smart contract.
- `event_name` (str): The name of the event to listen for.
- Returns:
  - `List[Dict[str, Any]]`: A list of dictionaries containing event data.

### Blockchain Information

#### `get_block(block_identifier: Union[int, str]) -> Dict[str, Any]`

Get information about a block.

- `block_identifier` (Union[int, str]): The block number or hash.
- Returns:
  - `Dict[str, Any]`: A dictionary containing information about the block.

#### `get_transaction(tx_hash: str) -> Dict[str, Any]`

Get information about a transaction.

- `tx_hash` (str): The hash of the transaction.
- Returns:
  - `Dict[str, Any]`: A dictionary containing information about the transaction.

#### `get_blockchain_version() -> str`

Get the version of the connected blockchain.

- Returns:
  - `str`: The version of the connected blockchain.

### Utility Methods

#### `is_valid_address(address: str) -> bool`

Check if an address is a valid Ethereum address.

- `

address` (str): The address to validate.
- Returns:
  - `bool`: True if the address is valid, False otherwise.

#### `to_wei(amount: Union[int, float], unit: str = 'ether') -> int`

Convert an amount from Ether to Wei.

- `amount` (Union[int, float]): The amount to convert.
- `unit` (str, optional): The unit of the amount ('ether' or 'gwei').
- Returns:
  - `int`: The amount converted to Wei.

#### `from_wei(amount: int, unit: str = 'ether') -> Union[int, float]`

Convert an amount from Wei to Ether.

- `amount` (int): The amount to convert.
- `unit` (str, optional): The unit to convert to ('ether' or 'gwei').
- Returns:
  - `Union[int, float]`: The amount converted to the specified unit.

This concludes the Usage Guide for the EthOrb package. If you have any further questions or need assistance, please don't hesitate to raise an [issue](https://github.com/sambitpoddar/ethorb/issues).
