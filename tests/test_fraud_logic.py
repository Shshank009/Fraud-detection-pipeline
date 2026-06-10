import unittest
import sys
sys.path.insert(0, '.')
from fraud_logic import check_fraud, get_rules_summary

class TestFraudLogic(unittest.TestCase):

    def test_high_amount(self):
        transaction = {'transaction_id': 'T1', 'account_id': 'A1', 'amount': 15000, 'country': 'GB', 'hour': 10}
        is_fraud, reason = check_fraud(transaction)
        self.assertTrue(is_fraud)
        self.assertEqual(reason, 'HIGH_AMOUNT')

    def test_normal_transaction(self):
        transaction = {'transaction_id': 'T2', 'account_id': 'A2', 'amount': 250, 'country': 'GB', 'hour': 14}
        is_fraud, reason = check_fraud(transaction)
        self.assertFalse(is_fraud)
        self.assertEqual(reason, 'NORMAL')

    def test_suspicious_location(self):
        transaction = {'transaction_id': 'T3', 'account_id': 'A3', 'amount': 500, 'country': 'XX', 'hour': 15}
        is_fraud, reason = check_fraud(transaction)
        self.assertTrue(is_fraud)
        self.assertEqual(reason, 'SUSPICIOUS_LOCATION')

    def test_odd_hours(self):
        transaction = {'transaction_id': 'T4', 'account_id': 'A4', 'amount': 750, 'country': 'GB', 'hour': 2}
        is_fraud, reason = check_fraud(transaction)
        self.assertTrue(is_fraud)
        self.assertEqual(reason, 'ODD_HOURS')

    def test_missing_fields(self):
        transaction = {'amount': 500, 'country': 'GB', 'hour': 10}
        is_fraud, reason = check_fraud(transaction)
        self.assertTrue(is_fraud)
        self.assertEqual(reason, 'MISSING_FIELDS')

    def test_boundary_amount(self):
        transaction = {'transaction_id': 'T5', 'account_id': 'A5', 'amount': 10000, 'country': 'GB', 'hour': 10}
        is_fraud, reason = check_fraud(transaction)
        self.assertFalse(is_fraud)
        self.assertEqual(reason, 'NORMAL')

    def test_rules_summary(self):
        summary = get_rules_summary()
        self.assertIn('HIGH_AMOUNT', summary)
        self.assertIn('SUSPICIOUS_LOCATION', summary)
        self.assertIn('ODD_HOURS', summary)
        self.assertIn('MISSING_FIELDS', summary)

if __name__ == '__main__':
    unittest.main()
