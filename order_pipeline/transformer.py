import re

def clean_price(value):
    """Extract numeric part from prices like 'N2500', '$35', '45 dollars'."""
    if isinstance(value, (int, float)):
        return float(value)

    if not isinstance(value, str):
        return 0.0

    # find numbers using regex
    match = re.findall(r"\d+\.?\d*", value)
    if not match:
        return 0.0

    return float(match[0])

def transform_orders(data):
    """Transform and normalize order records."""
    transformed = []

    for record in data:
        new_record = record.copy()

        # Clean numeric values
        new_record["quantity"] = clean_price(record.get("quantity", 0))
        new_record["price"] = clean_price(record.get("price", 0))
        new_record["total"] = round(new_record["quantity"] * new_record["price"], 2)

        # Normalize payment status
        status = str(record.get("payment_status", "")).strip().lower()
        if status in ["paid", "pending", "refunded", "refund"]:
            new_record["payment_status"] = status if status != "refund" else "refunded"
        else:
            new_record["payment_status"] = "unknown"

        # Clean text fields
        if "item" in record:
            new_record["item"] = record["item"].strip().title()

        transformed.append(new_record)

    return transformed
