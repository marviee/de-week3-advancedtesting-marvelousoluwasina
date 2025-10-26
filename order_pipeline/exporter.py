import json
import os


def export_to_json(data, output_path):
    """
    Exports cleaned data to a JSON file.
    Raises ValueError for invalid data or path.
    """
    if not isinstance(data, (list, dict)):
        raise ValueError("Data must be a list or dictionary")

    if not output_path.endswith(".json"):
        raise ValueError("Only JSON export is supported")

    directory = os.path.dirname(output_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except (OSError, TypeError, ValueError) as e:
        raise ValueError(f"Failed to export data: {e}")


def read_exported_file(path):
    """
    Helper function for testing.
    Reads and returns JSON content from a given file.
    """
    if not os.path.exists(path):
        raise FileNotFoundError("File does not exist")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
