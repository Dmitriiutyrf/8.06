import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

from core.db import Database
from core.catalog import Catalog
from core.access import AccessManager
from core.delivery import package_product
from adapters.telegram_stars import TelegramStarsAdapter

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load env
load_dotenv()
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not API_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in environment.")

# Init core
db = Database("data.db")
catalog = Catalog("catalog.json")
access = AccessManager(db, catalog)

# Init bot
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
adapter = TelegramStarsAdapter(bot)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    welcome = (
        "🚀 **Shadow Suite Storefront**\n\n"
        "Добро пожаловать в центр управления твоей цифровой фабрикой.\n"
        "Используй меню ниже, чтобы просмотреть доступные инструменты."
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Каталог продуктов", callback_data="catalog")],
        [InlineKeyboardButton(text="📦 Мои покупки", callback_data="my_purchases")]
    ])
    await message.answer(welcome, reply_markup=kb, parse_mode="Markdown")

@dp.message(Command("products"))
@dp.callback_query(F.data == "catalog")
async def show_products(event):
    products = catalog.list_all()
    text = "🔥 **Доступные инструменты:**"
    buttons = []
    for p in products:
        buttons.append([InlineKeyboardButton(
            text=f"{p['title']} — {p['price_xtr']} ⭐",
            callback_data=f"details_{p['id']}"
        )])

    kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    if isinstance(event, types.CallbackQuery):
        await event.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
    else:
        await event.answer(text, reply_markup=kb, parse_mode="Markdown")

@dp.callback_query(F.data.startswith("details_"))
async def product_details(callback: types.CallbackQuery):
    pid = callback.data.split("_")[1]
    product = catalog.get_product(pid)

    if product:
        has_access = access.has_access(callback.from_user.id, pid)
        text = (
            f"🛠 **{product['title']}**\n\n"
            f"{product['description']}\n\n"
            f"💰 **Цена:** {product['price_xtr']} ⭐"
        )

        btns = []
        if has_access:
            text += "\n\n✅ *У тебя уже есть доступ к этому продукту.*"
            btns.append([InlineKeyboardButton(text="📥 Забрать контент", callback_data=f"get_{pid}")])
        else:
            btns.append([InlineKeyboardButton(text=f"💳 Купить за {product['price_xtr']} ⭐", callback_data=f"buy_{pid}")])

        btns.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="catalog")])
        await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=btns), parse_mode="Markdown")

@dp.callback_query(F.data.startswith("buy_"))
async def buy_product(callback: types.CallbackQuery):
    pid = callback.data.split("_")[1]
    product = catalog.get_product(pid)
    if product:
        await adapter.create_invoice(callback.message.chat.id, product)
        await callback.answer()

@dp.pre_checkout_query()
async def on_pre_checkout(query: types.PreCheckoutQuery):
    ok, error = await adapter.confirm_payment(query, catalog)
    if ok:
        await query.answer(ok=True)
    else:
        await query.answer(ok=False, error_message=error)

@dp.callback_query(F.data.startswith("get_"))
async def deliver_product(callback: types.CallbackQuery):
    pid = callback.data.split("_")[1]
    user_id = callback.from_user.id

    if access.has_access(user_id, pid):
        await callback.message.answer(f"📦 Собираю пакет {pid} для тебя...")
        zip_path, err = package_product(pid)
        if zip_path:
            file = types.FSInputFile(zip_path)
            await bot.send_document(user_id, file, caption=f"Твой продукт {pid} готов!")
        else:
            await callback.message.answer(f"❌ Ошибка: {err}")
    else:
        await callback.answer("У тебя нет доступа к этому продукту.", show_alert=True)
    await callback.answer()

@dp.message(F.successful_payment)
async def on_successful_payment(message: types.Message):
    payment = message.successful_payment
    product_id = payment.invoice_payload
    charge_id = payment.telegram_payment_charge_id

    is_new = access.grant_access(message.from_user.id, product_id, charge_id)
    product = catalog.get_product(product_id)

    if is_new:
        await message.answer(
            f"🎉 **Успешная оплата!**\n\nТы приобрел: *{product['title']}*\n\n"
            "Нажми кнопку ниже, чтобы получить ZIP-архив с продуктом.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📥 Скачать продукт", callback_data=f"get_{product_id}")]
            ]),
            parse_mode="Markdown"
        )
    else:
        await message.answer("Доступ подтвержден. Твоя кнопка скачивания выше.")

@dp.message(Command("my"))
@dp.callback_query(F.data == "my_purchases")
async def show_purchases(event):
    user_id = event.from_user.id
    items = access.get_user_deliverables(user_id)

    if not items:
        text = "🤷‍♂️ У тебя пока нет купленных продуктов."
    else:
        text = "📦 **Твоя библиотека:**\n\n"
        for item in items:
            text += f"🔹 *{item['title']}*\n🔗 {item['deliverable']}\n\n"

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ В начало", callback_data="catalog")]
    ])

    if isinstance(event, types.CallbackQuery):
        await event.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
    else:
        await event.answer(text, reply_markup=kb, parse_mode="Markdown")

async def main():
    logger.info("Starting Shadow Storefront Bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
