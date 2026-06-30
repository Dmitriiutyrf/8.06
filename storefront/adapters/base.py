from abc import ABC, abstractmethod

class PaymentAdapter(ABC):
    @abstractmethod
    async def create_invoice(self, chat_id, product):
        """Sends an invoice to the user."""
        pass

    @abstractmethod
    async def confirm_payment(self, pre_checkout_query, catalog):
        """Validates the pre-checkout query."""
        pass
