import json

def read_json(file_path):
    """Reads a JSON file and returns a list of records."""
    if not file_path.endswith('.json'):
        raise ValueError('File format not supported')

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        raise ValueError('File not found')
    except Exception:
        raise ValueError('Invalid JSON')

    if not data:
        raise ValueError('File is empty')
    if not isinstance(data, list):
        raise ValueError('Expected a list of records')

    return data
