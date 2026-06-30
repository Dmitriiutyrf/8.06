# 🛒 Shadow Storefront

Единый узел продаж для продуктов Shadow Suite с поддержкой оплаты через **Telegram Stars**.

## Архитектура
Система построена на принципе «ядро + адаптеры», что позволяет легко добавлять новые способы оплаты (TON, ЮKassa), не затрагивая логику выдачи доступа.

- `core/`: Логика базы данных, каталога и контроля доступа.
- `adapters/`: Провайдеры платежей (начинаем с Telegram Stars).
- `catalog.json`: Конфигурация продуктов и цен.

## Установка
1. Создай бота в [@BotFather](https://t.me/BotFather) и получи токен.
2. Скопируй `.env.example` в `.env` и вставь токен:
   ```bash
   cp storefront/.env.example storefront/.env
   ```
3. Установи зависимости:
   ```bash
   pip install -r storefront/requirements.txt
   ```

## Запуск
```bash
python storefront/bot.py
```

## Добавление продуктов
Просто добавь новый объект в `storefront/catalog.json`. Поля:
- `id`: Уникальный идентификатор (используется для payload).
- `title`: Название для инвойса.
- `description`: Описание продукта.
- `price_xtr`: Цена в Telegram Stars.
- `deliverable`: Ссылка или текст, выдаваемый после оплаты.

---
*Created for Dmitry Digital Factory (June 2026)*
