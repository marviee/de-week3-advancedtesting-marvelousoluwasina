import os
import json
import pytest
from order_pipeline.pipeline import run_pipeline


@pytest.fixture
def mock_input_file(tmp_path):
    data = [
        {"order_id": 1, "item": "Book", "quantity": 2, "price": "₦2500", "total": "₦5000", "payment_status": "PAID"},
        {"order_id": 2, "item": "Pen", "quantity": 3, "price": "$2", "total": "$-6", "payment_status": "Pending"},
        {"order_id": 3, "item": "Bag", "quantity": 1, "price": "45 dollars", "total": "45 dollars", "payment_status": "Refunded"},
    ]
    input_file = tmp_path / "shoplink.json"
    with open(input_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    return input_file


def test_run_pipeline_end_to_end(mock_input_file, tmp_path):
    """Runs the full pipeline and verifies all outputs."""
    result = run_pipeline(str(mock_input_file), output_dir=str(tmp_path))

    # Stage counts
    assert result["raw_count"] == 3
    assert result["transformed_count"] == result["valid_count"]

    # Analytics structure
    analytics = result["analytics"]
    assert "total_revenue" in analytics
    assert "average_revenue" in analytics
    assert "status_count" in analytics

    # Output files
    assert os.path.exists(result["cleaned_file"])
    assert os.path.exists(result["analysis_file"])

    # Cleaned file content check
    with open(result["cleaned_file"], "r", encoding="utf-8") as f:
        data = json.load(f)
        assert isinstance(data, list)
        

    # Analysis file content check
    with open(result["analysis_file"], "r", encoding="utf-8") as f:
        analysis_data = json.load(f)
        assert "total_revenue" in analysis_data
        assert "status_count" in analysis_data


def test_run_pipeline_with_missing_input():
    """Should raise FileNotFoundError for missing input."""
    with pytest.raises(FileNotFoundError):
        run_pipeline("nonexistent.json")


