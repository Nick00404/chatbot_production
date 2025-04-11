# core/utils.py

import os
import json
from datetime import datetime
from typing import Any, Dict, Optional


def load_json(file_path: str) -> Dict[str, Any]:
    """Load JSON data from a file safely."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"[load_json] File not found: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        raise ValueError(f"[load_json] Invalid JSON in {file_path}: {e}")
    except Exception as e:
        raise RuntimeError(f"[load_json] Unexpected error reading {file_path}: {e}")


def save_json(file_path: str, data: Dict[str, Any], overwrite: bool = True, verbose: bool = False) -> None:
    """Save data to a JSON file. Optionally prevent overwriting existing files."""
    if not overwrite and os.path.exists(file_path):
        raise FileExistsError(f"[save_json] File exists and overwrite=False: {file_path}")

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        if verbose:
            print(f"[save_json] Saved JSON to {file_path}")
    except TypeError as e:
        raise ValueError(f"[save_json] Data is not JSON serializable: {e}")
    except Exception as e:
        raise RuntimeError(f"[save_json] Failed to write to {file_path}: {e}")


def get_timestamp(fmt: str = '%Y-%m-%d %H:%M:%S') -> str:
    """Return the current timestamp formatted as a string."""
    try:
        return datetime.now().strftime(fmt)
    except Exception as e:
        raise ValueError(f"[get_timestamp] Invalid datetime format: {e}")


def ensure_dir(directory: str, verbose: bool = False) -> None:
    """Ensure a directory exists; create it if it doesn't."""
    try:
        os.makedirs(directory, exist_ok=True)
        if verbose:
            print(f"[ensure_dir] Ensured directory: {directory}")
    except Exception as e:
        raise RuntimeError(f"[ensure_dir] Failed to create directory {directory}: {e}")
