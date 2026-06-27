import os
import json
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

load_dotenv()

# Replace with your actual token in .env
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def load_products():
    with open("data/products.json", "r", encoding="utf-8") as f:
        return json.load(f)

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    welcome_text = (
        "💣 **Добро пожаловать в Shadow Hub!**\n\n"
        "Здесь ты можешь приобрести мощные автономные ИИ-инструменты для своей цифровой фабрики.\n"
        "Все продукты поставляются в виде готовых ZIP-папок (Dmitry Standard)."
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📂 Посмотреть каталог", callback_data="catalog")],
        [InlineKeyboardButton(text="💎 О Shadow Suite", callback_data="about")]
    ])
    await message.answer(welcome_text, reply_markup=keyboard, parse_mode="Markdown")

@dp.callback_query(lambda c: c.data == "catalog")
async def show_catalog(callback_query: types.CallbackQuery):
    products = load_products()
    text = "🚀 **Наш арсенал на сегодня:**"
    buttons = []
    for p in products:
        buttons.append([InlineKeyboardButton(text=f"{p['name']} — {p['price']}", callback_data=f"buy_{p['id']}")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback_query.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")

@dp.callback_query(lambda c: c.data.startswith("buy_"))
async def product_details(callback_query: types.CallbackQuery):
    product_id = callback_query.data.split("_")[1]
    products = load_products()
    product = next((p for p in products if p["id"] == product_id), None)

    if product:
        text = (
            f"🛠 **{product['name']}**\n\n"
            f"{product['description']}\n\n"
            f"💰 **Цена:** {product['price']}\n\n"
            "После оплаты ты мгновенно получишь ссылку на скачивание архива с кодом и инструкцией."
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💳 Оплатить (Test Mode)", callback_data=f"pay_{product['id']}")],
            [InlineKeyboardButton(text="⬅️ Назад в каталог", callback_data="catalog")]
        ])
        await callback_query.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")

@dp.callback_query(lambda c: c.data.startswith("pay_"))
async def process_payment(callback_query: types.CallbackQuery):
    # Simulated payment flow
    product_id = callback_query.data.split("_")[1]
    await callback_query.message.answer(
        f"✅ **Оплата принята!**\nГенерирую твой персональный пакет {product_id}...\nПожалуйста, подожди пару секунд."
    )
    # Here delivery.py would zip and send the file
    await callback_query.message.answer(
        f"📦 **Твой продукт готов!**\n\n[Скачать {product_id}.zip](https://example.com/download/{product_id})\n\n*Это симуляция доставки. В реальной версии файл придет документом.*"
    )

async def main():
    print("Shadow Hub Bot is starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
