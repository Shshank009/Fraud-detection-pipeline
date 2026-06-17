import json
import logging
import boto3
from fraud_logic import check_fraud
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# AWS Configuration
S3_BUCKET = 'fraud-detection-transactions-shashhyy'
S3_FILE_KEY = 'sample_transactions.json'
DYNAMODB_TABLE = 'fraud_results'
SNS_TOPIC_ARN = 'arn:aws:sns:ap-south-1:326158158021:fraud-alerts'
AWS_REGION = 'ap-south-1'

# Initialize AWS clients
s3_client = boto3.client('s3', region_name=AWS_REGION)
dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
sns_client = boto3.client('sns', region_name=AWS_REGION)

def load_transactions_from_s3():
    """Load transactions from S3 bucket"""
    logger.info(f"Loading transactions from S3: {S3_BUCKET}/{S3_FILE_KEY}")
    try:
        response = s3_client.get_object(Bucket=S3_BUCKET, Key=S3_FILE_KEY)
        content = response['Body'].read().decode('utf-8')
        transactions = json.loads(content)
        logger.info(f"Successfully loaded {len(transactions)} transactions from S3")
        return transactions
    except Exception as e:
        logger.error(f"Error loading from S3: {str(e)}")
        raise

def save_to_dynamodb(transaction, reason):
    """Save flagged transaction to DynamoDB"""
    try:
        table = dynamodb.Table(DYNAMODB_TABLE)
        item = {
            'transaction_id': transaction['transaction_id'],
            'account_id': transaction['account_id'],
            'amount': str(transaction['amount']),
            'country': transaction['country'],
            'hour': str(transaction['hour']),
            'description': transaction.get('description', ''),
            'fraud_reason': reason,
            'flagged_at': datetime.utcnow().isoformat()
        }
        table.put_item(Item=item)
        logger.info(f"Saved flagged transaction {transaction['transaction_id']} to DynamoDB")
    except Exception as e:
        logger.error(f"Error saving to DynamoDB: {str(e)}")
        raise

def send_sns_alert(transaction, reason):
    """Send SNS alert for flagged transaction"""
    try:
        message = f"""
🚨 FRAUD ALERT - SecureBank Fraud Detection System

Transaction ID  : {transaction['transaction_id']}
Account ID      : {transaction['account_id']}
Amount          : £{transaction['amount']}
Country         : {transaction['country']}
Hour            : {transaction['hour']}:00
Description     : {transaction.get('description', 'N/A')}
Fraud Reason    : {reason}
Flagged At      : {datetime.utcnow().isoformat()} UTC

Please investigate this transaction immediately.

-- SecureBank Fraud Detection System
        """
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject=f'🚨 Fraud Alert - Transaction {transaction["transaction_id"]}'
        )
        logger.info(f"SNS alert sent for transaction {transaction['transaction_id']}")
    except Exception as e:
        logger.error(f"Error sending SNS alert: {str(e)}")
        raise

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
            'description': transaction.get('description', ''),
            'is_fraud': is_fraud,
            'reason': reason
        }

        if is_fraud:
            flagged_count += 1
            logger.warning(f"🚨 FRAUD DETECTED - Transaction: {transaction['transaction_id']} | Amount: £{transaction['amount']} | Reason: {reason}")

            # Save to DynamoDB
            save_to_dynamodb(transaction, reason)

            # Send SNS alert
            send_sns_alert(transaction, reason)
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

    # Load transactions from S3
    transactions = load_transactions_from_s3()

    # Process transactions
    results, flagged_count = process_transactions(transactions)

    # Print summary
    print_summary(results, flagged_count)

    logger.info("Fraud Detection Pipeline completed.")
