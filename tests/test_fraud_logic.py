import unittest
import sys
sys.path.insert(0, '.')
from fraud_logic import check_fraud

class TestFraudLogic(unittest.TestCase):

    def test_high_amount(self):
        transaction = {'amount': 15000, 'country': 'GB', 'hour': 10}
        is_fraud, reason = check_fraud(transaction)
        self.assertTrue(is_fraud)
        self.assertEqual(reason, 'HIGH_AMOUNT')

    def test_normal_transaction(self):
        transaction = {'amount': 250, 'country': 'GB', 'hour': 14}
        is_fraud, reason = check_fraud(transaction)
        self.assertFalse(is_fraud)
        self.assertEqual(reason, 'NORMAL')

    def test_suspicious_location(self):
        transaction = {'amount': 500, 'country': 'XX', 'hour': 15}
        is_fraud, reason = check_fraud(transaction)
        self.assertTrue(is_fraud)
        self.assertEqual(reason, 'SUSPICIOUS_LOCATION')

    def test_odd_hours(self):
        transaction = {'amount': 750, 'country': 'GB', 'hour': 2}
        is_fraud, reason = check_fraud(transaction)
        self.assertTrue(is_fraud)
        self.assertEqual(reason, 'ODD_HOURS')

if __name__ == '__main__':
    unittest.main()
