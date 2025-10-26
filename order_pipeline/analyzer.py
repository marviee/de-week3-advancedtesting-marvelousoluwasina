def analyze_orders(data):
    """Analyze cleaned order records and compute key metrics."""
    if not isinstance(data, list):
        raise ValueError("Input must be a list")

    if not data:
        return {
            "total_revenue": 0.0,
            "average_revenue": 0.0,
            "average_paid_revenue": 0.0,
            "total_pending": 0.0,
            "total_refunded": 0.0,
            "status_count": {"paid": 0, "pending": 0, "refunded": 0}
        }

    total_revenue = 0.0
    total_pending = 0.0
    total_refunded = 0.0
    paid_orders = 0
    totals = []
    status_count = {"paid": 0, "pending": 0, "refunded": 0}

    for record in data:
        status = str(record.get("payment_status", "")).lower().strip()
        total = float(record.get("total", 0))
        totals.append(total)

        # Count by status
        if status in status_count:
            status_count[status] += 1

        # Sum by category
        if status == "paid":
            total_revenue += total
            paid_orders += 1
        elif status == "pending":
            total_pending += total
        elif status == "refunded":
            total_refunded += total

    # Calculate averages
    avg_revenue = round(sum(totals) / len(totals), 2) if totals else 0.0
    avg_paid_revenue = round(total_revenue / paid_orders, 2) if paid_orders else 0.0

    return {
        "total_revenue": round(total_revenue, 2),
        "average_revenue": avg_revenue,
        "average_paid_revenue": avg_paid_revenue,
        "total_pending": round(total_pending, 2),
        "total_refunded": round(total_refunded, 2),
        "status_count": status_count
    }
