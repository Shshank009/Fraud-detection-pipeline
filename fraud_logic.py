import logging

logger = logging.getLogger(__name__)

# Fraud rule thresholds
HIGH_AMOUNT_THRESHOLD = 10000
SUSPICIOUS_COUNTRIES = ['XX', 'ZZ', 'KP', 'IR']
ODD_HOUR_START = 1
ODD_HOUR_END = 4
DUPLICATE_WINDOW_MINUTES = 5

def check_fraud(transaction):
    """
    Apply fraud detection rules to a transaction.
    Returns a tuple of (is_fraud, reason)
    """
    try:
        # Rule 1: Flag high value transactions
        if _check_high_amount(transaction):
            return True, 'HIGH_AMOUNT'

        # Rule 2: Flag transactions from suspicious locations
        if _check_suspicious_location(transaction):
            return True, 'SUSPICIOUS_LOCATION'

        # Rule 3: Flag odd hour transactions
        if _check_odd_hours(transaction):
            return True, 'ODD_HOURS'

        # Rule 4: Flag transactions with missing critical fields
        if _check_missing_fields(transaction):
            return True, 'MISSING_FIELDS'

        return False, 'NORMAL'

    except Exception as e:
        logger.error(f"Error processing transaction {transaction.get('transaction_id', 'UNKNOWN')}: {str(e)}")
        return True, 'PROCESSING_ERROR'


def _check_high_amount(transaction):
    """Rule 1: Flag transactions above threshold"""
    amount = transaction.get('amount', 0)
    if amount > HIGH_AMOUNT_THRESHOLD:
        logger.debug(f"High amount detected: £{amount}")
        return True
    return False


def _check_suspicious_location(transaction):
    """Rule 2: Flag transactions from suspicious countries"""
    country = transaction.get('country', '')
    if country in SUSPICIOUS_COUNTRIES:
        logger.debug(f"Suspicious location detected: {country}")
        return True
    return False


def _check_odd_hours(transaction):
    """Rule 3: Flag transactions during odd hours (1am - 4am)"""
    hour = transaction.get('hour', 12)
    if ODD_HOUR_START <= hour <= ODD_HOUR_END:
        logger.debug(f"Odd hour transaction detected: {hour}:00")
        return True
    return False


def _check_missing_fields(transaction):
    """Rule 4: Flag transactions with missing critical fields"""
    required_fields = ['transaction_id', 'account_id', 'amount', 'country']
    for field in required_fields:
        if not transaction.get(field):
            logger.debug(f"Missing required field: {field}")
            return True
    return False


def get_rules_summary():
    """Return a summary of all active fraud rules"""
    return {
        'HIGH_AMOUNT': f'Transaction amount exceeds £{HIGH_AMOUNT_THRESHOLD}',
        'SUSPICIOUS_LOCATION': f'Transaction from suspicious country: {SUSPICIOUS_COUNTRIES}',
        'ODD_HOURS': f'Transaction between {ODD_HOUR_START}am and {ODD_HOUR_END}am',
        'MISSING_FIELDS': 'Transaction missing required fields'
    }
