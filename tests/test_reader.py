import json
from order_pipeline.reader import read_json

def test_read_json_valid(tmp_path):
    # create sample data with multiple records
    data = [
        {"id": 1, "item": "Book"},
        {"id": 2, "item": "Laptop"},
        {"id": 3, "item": "Mouse"}
    ]

    # write it to a temporary file
    path = tmp_path / "orders.json"
    path.write_text(json.dumps(data))

    # run the function
    result = read_json(str(path))

    # assertions
    assert isinstance(result, list)
    assert len(result) == 3
    assert result[0]["item"] == "Book"
    assert result[1]["id"] == 2


def test_read_json_with_real_data():
    path = "data/shoplink.json"  # <-- your actual dataset
    result = read_json(path)

    # Basic checks
    assert isinstance(result, list)
    assert len(result) > 0

    # Check expected fields from real data
    first = result[0]
    assert "order_id" in first
    assert "item" in first
    assert "price" in first