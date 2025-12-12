from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)
import os

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = -1000000000000  # ID канала @black_starmama


# --- START ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("❤️ Подписаться на канал", url="https://t.me/black_starmama")],
        [InlineKeyboardButton("🔄 Проверить подписку", callback_data="check_sub")]
    ]
    await update.message.reply_text(
        "Привет! Чтобы продолжить, подпишись на наш канал ❤️",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# --- CHECK SUB ---
async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
    
    if member.status in ["member", "administrator", "creator"]:
        await query.message.reply_text("Спасибо за подписку! ❤️")
        await show_menu(query, context)
    else:
        await query.answer("Вы не подписаны!", show_alert=True)


# --- MENU ---
async def show_menu(query, context):
    keyboard = [
        [InlineKeyboardButton("📚 Выбрать курс/гайд", callback_data="catalog")],
        [InlineKeyboardButton("⭐ Отзывы", callback_data="reviews")],
        [InlineKeyboardButton("💼 Наша визитка", callback_data="card")]
    ]
    await query.message.reply_text(
        "Главное меню:", 
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# --- CATALOG ---
PRODUCTS = {
    "guide_walk": {
        "title": "✨ Гайд по походке",
        "desc": "Научитесь красиво и уверенно ходить. Пошаговый гайд с видео.",
        "price": "490 ₽",
        "paylink": "https://your-yookassa-link.com"
    },
    "course_queen": {
        "title": "🔥 Курс «Королева походки»",
        "desc": "Полный курс коррекции походки\n+ растяжка + осанка.",
        "price": "1990 ₽",
        "paylink": "https://your-yookassa-link.com"
    }
}


async def show_catalog(query):
    keyboard = []
    for key, product in PRODUCTS.items():
        keyboard.append([InlineKeyboardButton(product["title"], callback_data=f"product:{key}")])

    await query.message.reply_text(
        "Выберите продукт:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# --- PRODUCT CARD ---
async def show_product_card(query, product_id):
    product = PRODUCTS[product_id]

    keyboard = [
        [InlineKeyboardButton("💳 Оплатить", url=product["paylink"])],
        [InlineKeyboardButton("👩‍💼 Отправить чек менеджеру", url="https://t.me/manager_username")]
    ]

    text = (
        f"**{product['title']}**\n\n"
        f"{product['desc']}\n\n"
        f"💰 Цена: *{product['price']}*"
    )

    await query.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# --- CALLBACK HANDLER ---
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    if data == "check_sub":
        await check_subscription(update, context)

    elif data == "catalog":
        await show_catalog(query)

    elif data == "reviews":
        await query.message.reply_text("Отзывы: https://t.me/your_reviews")

    elif data == "card":
        await query.message.reply_text("Наша визитка: https://t.me/your_card")

    elif data.startswith("product:"):
        product_id = data.split(":")[1]
        await show_product_card(query, product_id)


# --- MAIN ---
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))

    app.run_polling()


if __name__ == "__main__":
    main()
