import pytest
from order_pipeline.analyzer import analyze_orders


# --- VALIDATION TESTS ----------------------

def test_analyze_orders_invalid_input():
    with pytest.raises(ValueError):
        analyze_orders("not a list")


def test_analyze_orders_empty_list():
    result = analyze_orders([])
    assert result["total_revenue"] == 0.0
    assert result["average_revenue"] == 0.0
    assert result["average_paid_revenue"] == 0.0
    assert result["total_pending"] == 0.0
    assert result["total_refunded"] == 0.0
    assert result["status_count"]["paid"] == 0


# --- MAIN LOGIC TESTS ----------------------

def test_analyze_orders_with_all_statuses():
    data = [
        {"payment_status": "paid", "total": 100},
        {"payment_status": "pending", "total": 50},
        {"payment_status": "refunded", "total": 30},
        {"payment_status": "paid", "total": 70},
    ]
    result = analyze_orders(data)

    assert result["total_revenue"] == 170.0
    assert result["average_revenue"] == 62.5  # (100+50+30+70)/4
    assert result["average_paid_revenue"] == 85.0  # (170/2)
    assert result["total_pending"] == 50.0
    assert result["total_refunded"] == 30.0
    assert result["status_count"] == {"paid": 2, "pending": 1, "refunded": 1}


def test_analyze_orders_with_mixed_case_and_spaces():
    data = [
        {"payment_status": " Paid ", "total": 60},
        {"payment_status": "  pending ", "total": 40},
        {"payment_status": "  REFUNDED ", "total": 20},
    ]
    result = analyze_orders(data)

    assert result["total_revenue"] == 60.0
    assert result["average_revenue"] == 40.0
    assert result["average_paid_revenue"] == 60.0
    assert result["total_pending"] == 40.0
    assert result["total_refunded"] == 20.0


def test_analyze_orders_unrecognized_status():
    data = [
        {"payment_status": "cancelled", "total": 100},
        {"payment_status": "Paid", "total": 40}
    ]
    result = analyze_orders(data)

    assert result["status_count"]["paid"] == 1
    assert result["total_revenue"] == 40.0
    assert result["average_paid_revenue"] == 40.0
    assert result["average_revenue"] == 70.0  # (100 + 40) / 2


# --- EDGE CASES ----------------------

def test_analyze_orders_no_paid_orders():
    data = [
        {"payment_status": "pending", "total": 50},
        {"payment_status": "refunded", "total": 30},
    ]
    result = analyze_orders(data)

    assert result["total_revenue"] == 0.0
    assert result["average_paid_revenue"] == 0.0
    assert result["total_pending"] == 50.0
    assert result["total_refunded"] == 30.0
    assert result["average_revenue"] == 40.0  # (50+30)/2


def test_analyze_orders_string_total_values():
    data = [
        {"payment_status": "paid", "total": "45"},
        {"payment_status": "pending", "total": "55.5"},
    ]
    result = analyze_orders(data)

    assert result["total_revenue"] == 45.0
    assert result["total_pending"] == 55.5
    assert result["average_paid_revenue"] == 45.0
    assert result["average_revenue"] == 50.25
