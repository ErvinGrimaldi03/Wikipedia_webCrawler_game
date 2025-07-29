from src._JSON import save_json, load_json
import re
import os

class PageDataStore:
    def __init__(self, base_dir="crawled_data"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def save_page_data(self, title, data):
        # Sanitize title for filename
        filename = os.path.join(self.base_dir, f"{self.sanitize_filename(title)}")
        save_json(data, filename)

    def load_page_data(self, title):
        filename = os.path.join(self.base_dir, f"{self.sanitize_filename(title)}")
        return load_json(filename)

    def sanitize_filename(self, title):
        return re.sub(r'[\\/:*?"<>|]', '_', title) # Replace invalid characters