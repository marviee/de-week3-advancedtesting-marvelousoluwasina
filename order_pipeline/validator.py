def validate_orders(data):
    """Validates list of order records and returns only valid ones."""
    if not isinstance(data, list):
        raise ValueError("Input must be a list of records")

    required_fields = ["order_id", "timestamp", "item", "quantity", "price", "payment_status", "total"]
    valid_records = []

    for record in data:
        # Skipping if not a dictionary
        if not isinstance(record, dict):
            continue

        # Checking for missing fields
        if not all(field in record for field in required_fields):
            continue

        # Checking numeric values
        try:
            quantity = float(record["quantity"])
            price = float(record["price"])
            total = float(record["total"])
        except (ValueError, TypeError):
            continue

        if quantity <= 0 or price <= 0 or total <= 0:
            continue

        # If everything is valid
        valid_records.append(record)

    return valid_records
