import json
import os

class Catalog:
    def __init__(self, catalog_path="catalog.json"):
        self.catalog_path = catalog_path
        self.products = self._load_catalog()

    def _load_catalog(self):
        if not os.path.exists(self.catalog_path):
            return []
        with open(self.catalog_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_product(self, product_id):
        """Returns product details by ID."""
        return next((p for p in self.products if p["id"] == product_id), None)

    def list_all(self):
        """Returns all products in the catalog."""
        return self.products
