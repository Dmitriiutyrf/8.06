from .base import PaymentAdapter
from aiogram import types

class TelegramStarsAdapter(PaymentAdapter):
    def __init__(self, bot):
        self.bot = bot

    async def create_invoice(self, chat_id, product):
        """Sends an invoice for Telegram Stars (XTR)."""
        await self.bot.send_invoice(
            chat_id=chat_id,
            title=product["title"],
            description=product["description"],
            payload=product["id"],
            provider_token="", # Empty for Stars
            currency="XTR",
            prices=[types.LabeledPrice(label=product["title"], amount=product["price_xtr"])]
        )

    async def confirm_payment(self, pre_checkout_query, catalog):
        """Validates that the product exists and the price is correct."""
        product_id = pre_checkout_query.invoice_payload
        product = catalog.get_product(product_id)

        if not product:
            return False, "Product not found."

        # In Stars, amount in pre_checkout is already in Stars
        if pre_checkout_query.total_amount != product["price_xtr"]:
            return False, "Price mismatch."

        return True, None
