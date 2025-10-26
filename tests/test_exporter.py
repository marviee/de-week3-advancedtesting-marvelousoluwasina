import os
import json
import pytest
from order_pipeline.exporter import export_to_json, read_exported_file


# ---------- FIXTURES ----------
@pytest.fixture
def sample_data():
    return [
        {"order_id": 1, "total": 100, "payment_status": "paid"},
        {"order_id": 2, "total": 50, "payment_status": "pending"},
    ]


@pytest.fixture
def output_file(tmp_path):
    return tmp_path / "shoplink_cleaned.json"


# ---------- TESTS FOR EXPORT FUNCTION ----------

def test_export_to_json_success(sample_data, output_file):
    """Should write JSON file successfully"""
    result = export_to_json(sample_data, str(output_file))
    assert result is True
    assert os.path.exists(output_file)

    # confirm content matches
    with open(output_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert isinstance(data, list)
        assert data[0]["order_id"] == 1


def test_export_to_json_invalid_type(tmp_path):
    """Should raise error for invalid data type"""
    invalid_data = "This is not a list or dict"
    path = tmp_path / "invalid.json"

    with pytest.raises(ValueError) as e:
        export_to_json(invalid_data, str(path))
    assert "Data must be" in str(e.value)


def test_export_to_json_invalid_extension(sample_data, tmp_path):
    """Should raise error for unsupported file format"""
    path = tmp_path / "output.txt"
    with pytest.raises(ValueError) as e:
        export_to_json(sample_data, str(path))
    assert "Only JSON export" in str(e.value)


def test_export_to_json_nonexistent_directory(sample_data, tmp_path):
    """Should create directory automatically if missing"""
    new_dir = tmp_path / "new_folder"
    path = new_dir / "output.json"
    result = export_to_json(sample_data, str(path))
    assert result is True
    assert os.path.exists(path)


def test_export_to_json_unserializable_data(tmp_path):
    """Should raise ValueError if data contains unserializable objects"""
    path = tmp_path / "bad.json"
    data = {"invalid": set([1, 2, 3])}  # sets cannot be JSON-serialized
    with pytest.raises(ValueError):
        export_to_json(data, str(path))


# ---------- TESTS FOR READ FUNCTION ----------

def test_read_exported_file_success(sample_data, output_file):
    """Should read exported JSON content correctly"""
    export_to_json(sample_data, str(output_file))
    result = read_exported_file(str(output_file))
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[1]["payment_status"] == "pending"


def test_read_exported_file_not_found(tmp_path):
    """Should raise error if file not found"""
    fake_path = tmp_path / "missing.json"
    with pytest.raises(FileNotFoundError):
        read_exported_file(str(fake_path))
