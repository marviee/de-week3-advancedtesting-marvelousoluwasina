import pytest
from order_pipeline.validator import validate_orders

def test_validate_orders_all_valid():
    data = [
        {"order_id": "1", "timestamp": "2025-10-25", "item": "Book", "quantity": 2, "price": 10, "payment_status": "Paid", "total": 20},
        {"order_id": "2", "timestamp": "2025-10-25", "item": "Pen", "quantity": 3, "price": 5, "payment_status": "Pending", "total": 15}
    ]
    result = validate_orders(data)
    assert len(result) == 2

def test_validate_orders_missing_field():
    data = [
        {"order_id": "1", "timestamp": "2025-10-25", "item": "Book", "quantity": 2, "price": 10}
    ]
    result = validate_orders(data)
    assert result == []

def test_validate_orders_negative_values():
    data = [
        {"order_id": "1", "timestamp": "2025-10-25", "item": "Book", "quantity": -1, "price": 10, "payment_status": "Paid", "total": -10}
    ]
    result = validate_orders(data)
    assert result == []

def test_validate_orders_non_list_input():
    with pytest.raises(ValueError):
        data = {"order_id": "1"}
        validate_orders(data)
        assert validate_orders(data) == []
