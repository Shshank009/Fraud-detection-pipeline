import json
import logging
from fraud_logic import check_fraud

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_transactions(filepath):
    """Load transactions from a JSON file"""
    logger.info(f"Loading transactions from {filepath}")
    with open(filepath, 'r') as f:
        transactions = json.load(f)
    logger.info(f"Loaded {len(transactions)} transactions")
    return transactions

def process_transactions(transactions):
    """Process each transaction and apply fraud rules"""
    results = []
    flagged_count = 0

    for transaction in transactions:
        is_fraud, reason = check_fraud(transaction)

        result = {
            'transaction_id': transaction['transaction_id'],
            'account_id': transaction['account_id'],
            'amount': transaction['amount'],
            'country': transaction['country'],
            'hour': transaction['hour'],
            'description': transaction['description'],
            'is_fraud': is_fraud,
            'reason': reason
        }

        if is_fraud:
            flagged_count += 1
            logger.warning(f"🚨 FRAUD DETECTED - Transaction: {transaction['transaction_id']} | Amount: £{transaction['amount']} | Reason: {reason}")
        else:
            logger.info(f"✅ NORMAL - Transaction: {transaction['transaction_id']} | Amount: £{transaction['amount']}")

        results.append(result)

    return results, flagged_count

def print_summary(results, flagged_count):
    """Print a summary of the fraud detection results"""
    total = len(results)
    print("\n" + "="*60)
    print("         FRAUD DETECTION SUMMARY")
    print("="*60)
    print(f"  Total Transactions Processed : {total}")
    print(f"  Normal Transactions          : {total - flagged_count}")
    print(f"  Flagged Transactions         : {flagged_count}")
    print("="*60)

    if flagged_count > 0:
        print("\n🚨 FLAGGED TRANSACTIONS:")
        print("-"*60)
        for r in results:
            if r['is_fraud']:
                print(f"  ID      : {r['transaction_id']}")
                print(f"  Account : {r['account_id']}")
                print(f"  Amount  : £{r['amount']}")
                print(f"  Reason  : {r['reason']}")
                print("-"*60)

if __name__ == '__main__':
    logger.info("Starting Fraud Detection Pipeline...")

    # Load transactions
    transactions = load_transactions('data/sample_transactions.json')

    # Process transactions
    results, flagged_count = process_transactions(transactions)

    # Print summary
    print_summary(results, flagged_count)

    logger.info("Fraud Detection Pipeline completed.")
