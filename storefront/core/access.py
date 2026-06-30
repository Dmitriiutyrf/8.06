from .db import Database
from .catalog import Catalog

class AccessManager:
    def __init__(self, db: Database, catalog: Catalog):
        self.db = db
        self.catalog = catalog

    def grant_access(self, user_id, product_id, charge_id):
        """Grants access to a product for a user."""
        return self.db.record_purchase(user_id, product_id, charge_id)

    def has_access(self, user_id, product_id):
        """Checks if a user has access to a product."""
        return self.db.check_access(user_id, product_id)

    def get_user_deliverables(self, user_id):
        """Returns a list of titles and deliverables for products owned by the user."""
        purchased_ids = self.db.get_user_purchases(user_id)
        results = []
        for pid in purchased_ids:
            product = self.catalog.get_product(pid)
            if product:
                results.append({
                    "title": product["title"],
                    "deliverable": product["deliverable"]
                })
        return results
