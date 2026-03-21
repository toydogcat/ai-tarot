import json
import os
import random

class ZhugeEngine:
    def __init__(self, data_path="data/zhuge/zhuge_data.json"):
        self.data_path = data_path
        self.zhuge_data = self._load_data()

    def _load_data(self):
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {self.data_path}: {e}")
            return []

    def draw_lot(self):
        if not self.zhuge_data:
            return None
        return random.choice(self.zhuge_data)
