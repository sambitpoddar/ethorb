import unittest
from ethorb import Blockchain

class TestBlockchain(unittest.TestCase):
    def setUp(self):
        # Set up any necessary test fixtures
        self.blockchain = Blockchain("https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID")

    def test_get_balance(self):
        # Test get_balance method
        balance = self.blockchain.get_balance("0x1234567890123456789012345678901234567890")
        self.assertIsInstance(balance, float)
        self.assertGreaterEqual(balance, 0.0)

    def test_send_transaction(self):
        # Test send_transaction method
        sender_address = "0x1234567890123456789012345678901234567890"
        recipient_address = "0x0987654321098765432109876543210987654321"
        amount = 1.0
        private_key = "YOUR_PRIVATE_KEY"
        tx_hash = self.blockchain.send_transaction(sender_address, recipient_address, amount, private_key)
        self.assertIsInstance(tx_hash, str)
        self.assertGreater(len(tx_hash), 0)

    # Add more test methods here

if __name__ == '__main__':
    unittest.main()
  
