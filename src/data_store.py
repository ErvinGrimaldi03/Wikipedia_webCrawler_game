# data_store.py
from src._JSON import save_json, load_json
import os
import re

class PageDataStore:
    """Manages storing and retrieving crawled Wikipedia page data."""

    def __init__(self, base_dir="crawled_data"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def save_page_data(self, title: str, data: dict):
        """Saves data for a specific Wikipedia page."""
        sanitized_title = self._sanitize_filename(title)
        # Pass the path *without* .json extension to save_json
        file_path_without_ext = os.path.join(self.base_dir, sanitized_title)
        save_json(data, file_path_without_ext)

    def load_page_data(self, title: str) -> dict | None:
        """Loads data for a specific Wikipedia page."""
        sanitized_title = self._sanitize_filename(title)
        # Pass the path *without* .json extension to load_json
        file_path_without_ext = os.path.join(self.base_dir, sanitized_title)
        return load_json(file_path_without_ext)

    def _sanitize_filename(self, title: str) -> str:
        """Sanitizes a title to be a valid filename."""
        sanitized = re.sub(r'[\\/:*?"<>|]', '_', title)
        # Ensure it's not empty after sanitization
        if not sanitized:
            sanitized = "untitled_page"
        return sanitized[:200] # Limit length to prevent issues on some file systems