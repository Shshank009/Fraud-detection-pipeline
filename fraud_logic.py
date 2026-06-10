def check_fraud(transaction):
    """
    Apply fraud detection rules to a transaction.
    Returns a tuple of (is_fraud, reason)
    """
    # Rule 1: Flag high value transactions
    if transaction['amount'] > 10000:
        return True, 'HIGH_AMOUNT'
    
    # Rule 2: Flag transactions from suspicious locations
    suspicious_countries = ['XX', 'ZZ']
    if transaction.get('country') in suspicious_countries:
        return True, 'SUSPICIOUS_LOCATION'
    
    # Rule 3: Flag odd hour transactions (1am - 4am)
    hour = transaction.get('hour', 12)
    if 1 <= hour <= 4:
        return True, 'ODD_HOURS'
    
    return False, 'NORMAL'
