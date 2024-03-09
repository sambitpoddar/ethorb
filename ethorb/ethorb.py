# EthOrb - A Python package for interacting with Ethereum blockchain networks.
# Author: Sambit Poddar
# License: Apache License 2.0
# ethorb.py

from web3 import Web3
from web3.exceptions import InvalidAddress, TransactionNotFound
from eth_utils import to_checksum_address, is_address
from eth_account import Account
from web3.middleware import geth_poa_middleware
from typing import Dict, Any, List, Union
from functools import wraps

class Blockchain:
    """A class for interacting with Ethereum blockchain networks."""

    def __init__(self, network_url: str):
        """Initialize the Blockchain instance with the specified network URL.

        Args:
            network_url (str): The URL of the Ethereum network to connect to.
        """
        self.web3 = Web3(Web3.HTTPProvider(network_url))
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.contract_abi = None  # Initialize the smart contract ABI attribute

    def set_contract_abi(self, contract_abi: Dict[str, Any]):
        """Set the ABI (Application Binary Interface) of a smart contract.

        Args:
            contract_abi (Dict[str, Any]): The ABI of the smart contract.
        """
        self.contract_abi = contract_abi

    def _validate_address(func):
        """Decorator function to validate Ethereum addresses."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            address = args[1] if len(args) > 1 else kwargs.get('address')
            if not address or not is_address(address):
                raise ValueError("Invalid Ethereum address provided.")
            return func(*args, **kwargs)
        return wrapper

    @_validate_address
    def get_balance(self, address: str) -> float:
        """Get the balance of a wallet address.

        Args:
            address (str): The Ethereum address to get the balance for.

        Returns:
            float: The balance of the address in Ether.
        """
        balance = self.web3.eth.get_balance(to_checksum_address(address))
        return self.web3.fromWei(balance, 'ether')

    @_validate_address
    def send_transaction(self, sender_address: str, recipient_address: str, amount: float, private_key: str, gas_limit: int = None, gas_price: int = None, data: bytes = None, nonce: int = None, chain_id: int = None) -> str:
        """Send cryptocurrency from one address to another.

        Args:
            sender_address (str): The sender's Ethereum address.
            recipient_address (str): The recipient's Ethereum address.
            amount (float): The amount of cryptocurrency to send, in Ether.
            private_key (str): The private key of the sender's Ethereum address.
            gas_limit (int, optional): The gas limit for the transaction.
            gas_price (int, optional): The gas price for the transaction.
            data (bytes, optional): Additional data to include in the transaction.
            nonce (int, optional): The nonce for the transaction.
            chain_id (int, optional): The chain ID for the transaction.

        Returns:
            str: The transaction hash of the sent transaction.
        """
        sender_address = to_checksum_address(sender_address)
        recipient_address = to_checksum_address(recipient_address)
        amount_wei = self.web3.toWei(amount, 'ether')

        if nonce is None:
            nonce = self.web3.eth.get_transaction_count(sender_address)

        if gas_limit is None:
            gas_limit = self.web3.eth.estimate_gas({'to': recipient_address, 'value': amount_wei})

        if gas_price is None:
            gas_price = self.web3.eth.gas_price

        if data is None:
            transaction = {
                'nonce': nonce,
                'to': recipient_address,
                'value': amount_wei,
                'gas': gas_limit,
                'gasPrice': gas_price,
            }
        else:
            transaction = {
                'nonce': nonce,
                'to': recipient_address,
                'value': amount_wei,
                'gas': gas_limit,
                'gasPrice': gas_price,
                'data': data,
            }

        if chain_id is not None:
            transaction['chainId'] = chain_id

        signed_txn = Account.sign_transaction(transaction, private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return tx_hash.hex()

    @_validate_address
    def deploy_contract(self, contract_code: Dict[str, Any], sender_address: str, private_key: str, gas_limit: int = None, gas_price: int = None, nonce: int = None, chain_id: int = None) -> str:
        """Deploy a smart contract to the blockchain.

        Args:
            contract_code (Dict[str, Any]): The bytecode and ABI of the smart contract.
            sender_address (str): The address deploying the contract.
            private_key (str): The private key of the sender's Ethereum address.
            gas_limit (int, optional): The gas limit for the transaction.
            gas_price (int, optional): The gas price for the transaction.
            nonce (int, optional): The nonce for the transaction.
            chain_id (int, optional): The chain ID for the transaction.

        Returns:
            str: The transaction hash of the contract deployment transaction.
        """
        sender_address = to_checksum_address(sender_address)
        contract = self.web3.eth.contract(abi=contract_code['abi'], bytecode=contract_code['bytecode'])

        if nonce is None:
            nonce = self.web3.eth.get_transaction_count(sender_address)

        if gas_limit is None:
            gas_limit = self.web3.eth.estimate_gas({'from': sender_address, 'data': contract_code['bytecode']})

        if gas_price is None:
            gas_price = self.web3.eth.gas_price

        txn_hash = contract.constructor().buildTransaction({'from': sender_address, 'nonce': nonce, 'gas': gas_limit, 'gasPrice': gas_price})

        if chain_id is not None:
            txn_hash['chainId'] = chain_id

        signed_txn = self.web3.eth.account.sign_transaction(txn_hash, private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return tx_hash.hex()

    def call_contract_function(self, contract_address: str, function_name: str, *args) -> Any:
        """Call a function of a smart contract.

        Args:
            contract_address (str): The address of the smart contract.
            function_name (str): The name of the function to call.
            *args: Arguments to pass to the function.

        Returns:
            Any: The result of the function call.
        """
        contract_address = to_checksum_address(contract_address)
        contract = self.web3.eth.contract(address=contract_address, abi=self.contract_abi)
        function = getattr(contract.functions, function_name)(*args)
        return function.call()

    def listen_for_events(self, contract_address: str, event_name: str) -> List[Dict[str, Any]]:
        """Listen for events emitted by a smart contract.

        Args:
            contract_address (str): The address of the smart contract.
            event_name (str): The name of the event to listen for.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing event data.
        """
        contract_address = to_checksum_address(contract_address)
        contract = self.web3.eth.contract(address=contract_address, abi=self.contract_abi)
        event_filter = contract.events[event_name].createFilter(fromBlock='latest')
        return event_filter.get_all_entries()

    def generate_wallet(self) -> Dict[str, str]:
        """Generate a new wallet address and private key.

        Returns:
            Dict[str, str]: A dictionary containing the new wallet address and private key.
        """
        account = self.web3.eth.account.create()
        return {
            'address': account.address,
            'private_key': account.privateKey.hex()
        }

    def is_valid_address(self, address: str) -> bool:
        """Check if an address is a valid Ethereum address.

        Args:
            address (str): The address to check.

        Returns:
            bool: True if the address is valid, False otherwise.
        """
        return is_address(address)

    def get_transaction_receipt(self, tx_hash: str) -> Dict[str, Any]:
        """Get the receipt of a transaction.

        Args:
            tx_hash (str): The hash of the transaction.

        Returns:
            Dict[str, Any]: A dictionary containing the transaction receipt.
        """
        try:
            tx_receipt = self.web3.eth.get_transaction_receipt(tx_hash)
            if tx_receipt:
                return tx_receipt
            else:
                raise ValueError("Transaction receipt not found.")
        except TransactionNotFound:
            raise ValueError("Transaction not found.")

    def get_block(self, block_identifier: Union[int, str]) -> Dict[str, Any]:
        """Get information about a block.

        Args:
            block_identifier (Union[int, str]): The block number or hash.

        Returns:
            Dict[str, Any]: A dictionary containing information about the block.
        """
        try:
            block = self.web3.eth.get_block(block_identifier)
            if block:
                return block
            else:
                raise ValueError("Block not found.")
        except ValueError:
            raise ValueError("Invalid block identifier.")

    def get_transaction(self, tx_hash: str) -> Dict[str, Any]:
        """Get information about a transaction.

        Args:
            tx_hash (str): The hash of the transaction.

        Returns:
            Dict[str, Any]: A dictionary containing information about the transaction.
        """
        try:
            tx = self.web3.eth.get_transaction(tx_hash)
            if tx:
                return tx
            else:
                raise ValueError("Transaction not found.")
        except TransactionNotFound:
            raise ValueError("Transaction not found.")

    def get_blockchain_version(self) -> str:
        """Get the version of the connected blockchain.

        Returns:
            str: The version of the connected blockchain.
        """
        return self.web3.clientVersion

    def get_gas_price(self) -> float:
        """Get the current gas price.

        Returns:
            float: The current gas price.
        """
        return self.web3.eth.gas_price

    def estimate_gas(self, transaction: Dict[str, Any]) -> int:
        """Estimate gas for a transaction.

        Args:
            transaction (Dict[str, Any]): The transaction details.

        Returns:
            int: The estimated gas for the transaction.
        """
        return self.web3.eth.estimate_gas(transaction)

    def get_current_block_number(self) -> int:
        """Get the current block number.

        Returns:
            int: The current block number.
        """
        return self.web3.eth.block_number

    def get_block_transaction_count(self, block_identifier: Union[int, str]) -> int:
        """Get the number of transactions in a block.

        Args:
            block_identifier (Union[int, str]): The block number or hash.

        Returns:
            int: The number of transactions in the block.
        """
        return self.web3.eth.get_block_transaction_count(block_identifier)

    def get_transaction_count(self, address: str, block_identifier: Union[int, str] = 'latest') -> int:
        """Get the number of transactions sent from an address.

        Args:
            address (str): The address to check.
            block_identifier (Union[int, str], optional): The block number or hash. Defaults to 'latest'.

        Returns:
            int: The number of transactions sent from the address.
        """
        address = to_checksum_address(address)
        return self.web3.eth.get_transaction_count(address, block_identifier)

    def get_contract_code(self, contract_address: str) -> Dict[str, Any]:
        """Get the code of a deployed contract.

        Args:
            contract_address (str): The address of the contract.

        Returns:
            Dict[str, Any]: A dictionary containing the code of the contract.
        """
        contract_address = to_checksum_address(contract_address)
        return self.web3.eth.get_code(contract_address)

    def get_contract_storage_at(self, contract_address: str, position: int, block_identifier: Union[int, str] = 'latest') -> bytes:
        """Get the storage at a specific position in a contract.

        Args:
            contract_address (str): The address of the contract.
            position (int): The position in the contract's storage.
            block_identifier (Union[int, str], optional): The block number or hash. Defaults to 'latest'.

        Returns:
            bytes: The storage data at the specified position.
        """
        contract_address = to_checksum_address(contract_address)
        return self.web3.eth.get_storage_at(contract_address, position, block_identifier)

    def get_past_logs(self, event_name: str, from_block: int = 0, to_block: Union[int, str] = 'latest', address: str = None, topics: List[str] = None) -> List[Dict[str, Any]]:
        """Get past logs that match the specified criteria.

        Args:
            event_name (str): The name of the event.
            from_block (int, optional): The starting block number. Defaults to 0.
            to_block (Union[int, str], optional): The ending block number or 'latest'. Defaults to 'latest'.
            address (str, optional): The address to filter logs by. Defaults to None.
            topics (List[str], optional): The topics to filter logs by. Defaults to None.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing the logs that match the criteria.
        """
        filter_params = {'fromBlock': from_block, 'toBlock': to_block}
        if address:
            filter_params['address'] = to_checksum_address(address)
        if topics:
            filter_params['topics'] = topics
        logs = self.web3.eth.get_logs(filter_params)
        return logs

    def get_block_uncles(self, block_identifier: Union[int, str]) -> List[Dict[str, Any]]:
        """Get the list of uncle blocks for a given block.

        Args:
            block_identifier (Union[int, str]): The block number or hash.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing information about uncle blocks.
        """
        block = self.get_block(block_identifier)
        uncles = block.get('uncles', [])
        return uncles

    def get_transaction_by_block_and_index(self, block_identifier: Union[int, str], transaction_index: int) -> Dict[str, Any]:
        """Get information about a transaction by block number or hash and transaction index.

        Args:
            block_identifier (Union[int, str]): The block number or hash.
            transaction_index (int): The index of the transaction in the block.

        Returns:
            Dict[str, Any]: A dictionary containing information about the transaction.
        """
        transaction = self.web3.eth.get_transaction_by_block(block_identifier, transaction_index)
        if transaction:
            return transaction
        else:
            raise ValueError("Transaction not found.")

    def get_block_by_hash(self, block_hash: str) -> Dict[str, Any]:
        """Get information about a block by its hash.

        Args:
            block_hash (str): The hash of the block.

        Returns:
            Dict[str, Any]: A dictionary containing information about the block.
        """
        block = self.web3.eth.get_block(block_hash)
        if block:
            return block
        else:
            raise ValueError("Block not found.")

    def get_block_by_number(self, block_number: int) -> Dict[str, Any]:
        """Get information about a block by its number.

        Args:
            block_number (int): The number of the block.

        Returns:
            Dict[str, Any]: A dictionary containing information about the block.
        """
        block = self.web3.eth.get_block(block_number)
        if block:
            return block
        else:
            raise ValueError("Block not found.")

    def get_transaction_count_by_block(self, block_identifier: Union[int, str]) -> int:
        """Get the number of transactions in a block.

        Args:
            block_identifier (Union[int, str]): The block number or hash.

        Returns:
            int: The number of transactions in the block.
        """
        block = self.get_block(block_identifier)
        return len(block.get('transactions', []))

    def get_block_uncle_count(self, block_identifier: Union[int, str]) -> int:
        """Get the number of uncles in a block.

        Args:
            block_identifier (Union[int, str]): The block number or hash.

        Returns:
            int: The number of uncles in the block.
        """
        block = self.get_block(block_identifier)
        return len(block.get('uncles', []))

    def get_block_transaction_hashes(self, block_identifier: Union[int, str]) -> List[str]:
        """Get transaction hashes in a block.

        Args:
            block_identifier (Union[int, str]): The block number or hash.

        Returns:
            List[str]: A list of transaction hashes in the block.
        """
        block = self.get_block(block_identifier)
        return block.get('transactions', [])

    def get_block_uncle_hashes(self, block_identifier: Union[int, str]) -> List[str]:
        """Get uncle hashes in a block.

        Args:
            block_identifier (Union[int, str]): The block number or hash.

        Returns:
            List[str]: A list of uncle hashes in the block.
        """
        block = self.get_block(block_identifier)
        return block.get('uncles', [])

    def get_block_transactions(self, block_identifier: Union[int, str]) -> List[Dict[str, Any]]:
        """Get transactions in a block.

        Args:
            block_identifier (Union[int, str]): The block number or hash.

        Returns:
            List[Dict[str, Any]]: A list of transaction objects in the block.
        """
        block = self.get_block(block_identifier)
        transactions = [self.get_transaction(tx_hash) for tx_hash in block['transactions']]
        return transactions

    def get_block_uncle_headers(self, block_identifier: Union[int, str]) -> List[Dict[str, Any]]:
        """Get uncle headers in a block.

        Args:
            block_identifier (Union[int, str]): The block number or hash.

        Returns:
            List[Dict[str, Any]]: A list of uncle header objects in the block.
        """
        block = self.get_block(block_identifier)
        uncle_headers = [self.get_block_by_hash(uncle_hash) for uncle_hash in block['uncles']]
        return uncle_headers

    def get_block_full_transactions(self, block_identifier: Union[int, str]) -> List[Dict[str, Any]]:
        """Get full transactions in a block (including transaction details).

        Args:
            block_identifier (Union[int, str]): The block number or hash.

        Returns:
            List[Dict[str, Any]]: A list of full transaction objects in the block.
        """
        block = self.get_block(block_identifier)
        full_transactions = [self.get_transaction(tx_hash) for tx_hash in block['transactions']]
        return full_transactions

    def get_block_transaction_count_by_type(self, block_identifier: Union[int, str], tx_type: str) -> int:
        """Get the number of transactions of a specific type in a block.

        Args:
            block_identifier (Union[int, str]): The block number or hash.
            tx_type (str): The type of transaction to count.

        Returns:
            int: The number of transactions of the specified type in the block.
        """
        block = self.get_block(block_identifier)
        tx_count = sum(1 for tx_hash in block['transactions'] if self.get_transaction(tx_hash)['type'] == tx_type)
        return tx_count
        
    def get_block_uncle_count_by_type(self, block_identifier: Union[int, str], uncle_type: str) -> int:
        """Get the number of uncles of a specific type in a block.

        Args:
            block_identifier (Union[int, str]): The block number or hash.
            uncle_type (str): The type of uncle to count.

        Returns:
            int: The number of uncles of the specified type in the block.
        """
        block = self.get_block(block_identifier)
        uncle_count = sum(1 for uncle_hash in block['uncles'] if self.get_block_by_hash(uncle_hash)['type'] == uncle_type)
        return uncle_count

    def get_block_transaction_senders(self, block_identifier: Union[int, str]) -> List[str]:
        """Get the addresses of transaction senders in a block.

        Args:
            block_identifier (Union[int, str]): The block number or hash.

        Returns:
            List[str]: A list of addresses of transaction senders in the block.
        """
        block = self.get_block(block_identifier)
        senders = [self.get_transaction(tx_hash)['from'] for tx_hash in block['transactions']]
        return senders

    def get_block_transaction_recipients(self, block_identifier: Union[int, str]) -> List[str]:
        """Get the addresses of transaction recipients in a block.

        Args:
            block_identifier (Union[int, str]): The block number or hash.

        Returns:
            List[str]: A list of addresses of transaction recipients in the block.
        """
        block = self.get_block(block_identifier)
        recipients = [self.get_transaction(tx_hash)['to'] for tx_hash in block['transactions'] if self.get_transaction(tx_hash)['to'] is not None]
        return recipients

    def get_block_uncle_senders(self, block_identifier: Union[int, str]) -> List[str]:
        """Get the addresses of uncle senders in a block.

        Args:
            block_identifier (Union[int, str]): The block number or hash.

        Returns:
            List[str]: A list of addresses of uncle senders in the block.
        """
        uncle_headers = self.get_block_uncle_headers(block_identifier)
        senders = [uncle_header['miner'] for uncle_header in uncle_headers]
        return senders

    def get_block_uncle_rewards(self, block_identifier: Union[int, str]) -> List[float]:
        """Get the rewards of uncle blocks in a block.

        Args:
            block_identifier (Union[int, str]): The block number or hash.

        Returns:
            List[float]: A list of rewards of uncle blocks in the block.
        """
        uncle_headers = self.get_block_uncle_headers(block_identifier)
        rewards = [float(uncle_header['reward']) for uncle_header in uncle_headers]
        return rewards

    def get_block_uncle_times(self, block_identifier: Union[int, str]) -> List[int]:
        """Get the timestamps of uncle blocks in a block.

        Args:
            block_identifier (Union[int, str]): The block number or hash.

        Returns:
            List[int]: A list of timestamps of uncle blocks in the block.
        """
        uncle_headers = self.get_block_uncle_headers(block_identifier)
        times = [uncle_header['timestamp'] for uncle_header in uncle_headers]
        return times

    def get_block_gas_used(self, block_identifier: Union[int, str]) -> int:
        """Get the gas used by a block.

        Args:
            block_identifier (Union[int, str]): The block number or hash.

        Returns:
            int: The gas used by the block.
        """
        block = self.get_block(block_identifier)
        return block['gasUsed']

    def get_block_difficulty(self, block_identifier: Union[int, str]) -> int:
        """Get the difficulty of a block.

        Args:
            block_identifier (Union[int, str]): The block number or hash.

        Returns:
            int: The difficulty of the block.
        """
        block = self.get_block(block_identifier)
        return block['difficulty']

    def get_block_total_difficulty(self, block_identifier: Union[int, str]) -> int:
        """Get the total difficulty of a block.

        Args:
            block_identifier (Union[int, str]): The block number or hash.

        Returns:
            int: The total difficulty of the block.
        """
        block = self.get_block(block_identifier)
        return block['totalDifficulty']

    def get_block_timestamp(self, block_identifier: Union[int, str]) -> int:
        """Get the timestamp of a block.

        Args:
            block_identifier (Union[int, str]): The block number or hash.

        Returns:
            int: The timestamp of the block.
        """
        block = self.get_block(block_identifier)
        return block['timestamp']

    def get_block_gas_limit(self, block_identifier: Union[int, str]) -> int:
        """Get the gas limit of a block.

        Args:
            block_identifier (Union[int, str]): The block number or hash.

        Returns:
            int: The gas limit of the block.
        """
        block = self.get_block(block_identifier)
        return block['gasLimit']

    def get_block_nonce(self, block_identifier: Union[int, str]) -> int:
        """Get the nonce of a block.

        Args:
            block_identifier (Union[int, str]): The block number or hash.

        Returns:
            int: The nonce of the block.
        """
        block = self.get_block(block_identifier)
        return block['nonce']

    def get_block_sha3_uncles(self, block_identifier: Union[int, str]) -> str:
        """Get the SHA3 uncles of a block.

        Args:
            block_identifier (Union[int, str]): The block number or hash.

        Returns:
            str: The SHA3 uncles of the block.
        """
        block = self.get_block(block_identifier)
        return block['sha3Uncles']

    def get_block_logs_bloom(self, block_identifier: Union[int, str]) -> str:
        """Get the logs bloom of a block.

        Args:
            block_identifier (Union[int, str]): The block number or hash.

        Returns:
            str: The logs bloom of the block.
        """
        block = self.get_block(block_identifier)
        return block['logsBloom']

    def get_block_miner(self, block_identifier: Union[int, str]) -> str:
        """Get the miner of a block.

        Args:
            block_identifier (Union[int, str]): The block number or hash.

        Returns:
            str: The miner of the block.
        """
        block = self.get_block(block_identifier)
        return block['miner']

    def get_block_mix_hash(self, block_identifier: Union[int, str]) -> str:
        """Get the mix hash of a block.

        Args:
            block_identifier (Union[int, str]): The block number or hash.

        Returns:
            str: The mix hash of the block.
        """
        block = self.get_block(block_identifier)
        return block['mixHash']

    def get_block_transactions_root(self, block_identifier: Union[int, str]) -> str:
        """Get the transactions root of a block.

        Args:
            block_identifier (Union[int, str]): The block number or hash.

        Returns:
            str: The transactions root of the block.
        """
        block = self.get_block(block_identifier)
        return block['transactionsRoot']

    def get_block_state_root(self, block_identifier: Union[int, str]) -> str:
        """Get the state root of a block.

        Args:
            block_identifier (Union[int, str]): The block number or hash.

        Returns:
            str: The state root of the block.
        """
        block = self.get_block(block_identifier)
        return block['stateRoot']

    def get_block_receipts_root(self, block_identifier: Union[int, str]) -> str:
        """Get the receipts root of a block.

        Args:
            block_identifier (Union[int, str]): The block number or hash.

        Returns:
            str: The receipts root of the block.
        """
        block = self.get_block(block_identifier)
        return block['receiptsRoot']

    def get_block_uncles_count(self, block_identifier: Union[int, str]) -> int:
        """Get the count of uncles in a block.

        Args:
            block_identifier (Union[int, str]): The block number or hash.

        Returns:
            int: The count of uncles in the block.
        """
        block = self.get_block(block_identifier)
        return len(block['uncles'])
        
# Hi, I am Sambit. Congratulations, you have reached the end of the code!  
