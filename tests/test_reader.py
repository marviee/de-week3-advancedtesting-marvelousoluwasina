import json
import pytest
from order_pipeline.reader import read_json

def test_read_json_valid(tmp_path):
    # created sample data with multiple records
    data = [
        {"id": 1, "item": "Book"},
        {"id": 2, "item": "Laptop"},
        {"id": 3, "item": "Mouse"}
    ]

    # write itt to a temporary file
    path = tmp_path / "orders.json"
    path.write_text(json.dumps(data))

    # run the function
    result = read_json(str(path))

    # assertions
    assert isinstance(result, list)
    assert len(result) == 3
    assert result[0]["item"] == "Book"
    assert result[1]["id"] == 2

# def test_FileNotFoundError(tmp_path):
#     with pytest.raises(ValueError('File format not supported')
# ):
#         path = tmp_path / "orders.csv"
        
        
