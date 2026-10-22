import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

TOKEN = os.environ.get("TELEGRAM_TOKEN")

# صور أنمي جاهزة وجميلة للتفاعل
ANIME_IMAGES = [
    "https://images.unsplash.com/photo-1578632767115-351597cf2477?w=600",
    "https://images.unsplash.com/photo-1563089145-599997674d42?w=600",
    "https://images.unsplash.com/photo-1604200213928-ba3cf4fc8436?w=600"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎨 تحويل صورتي لأنمي", callback_data="convert_anime")],
        [InlineKeyboardButton("⭐ شخصيات أنمي عشوائية", callback_data="random_anime")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "أهلاً بك في عالم **الأنمي الساحر!** 🌸🎌\n\nأرسل لي صورتك الشخصية أو اضغط على الأزرار في الأسفل لنبدأ المتعة!"
    
    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")
    elif update.callback_query:
        query = update.callback_query
        await query.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "convert_anime":
        text = "📸 **أرسل صورتك الآن في المحادثة!**\n\nدعني أرى ملامحك لكي أقوم بتحويلها إلى بطل أنمي أسطوري ✨"
        await query.message.reply_text(text, parse_mode="Markdown")
    elif data == "random_anime":
        caption = "✨ **إليك إحدى شخصيات الأنمي المميزة اليوم!**"
        keyboard = [[InlineKeyboardButton("🔄 صورة أخرى", callback_data="random_anime"), InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_photo(photo=ANIME_IMAGES[0], caption=caption, reply_markup=reply_markup, parse_mode="Markdown")
    elif data == "main_menu":
        await start(update, context)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # عندما يرسل المستخدم صورة، يقوم البوت بالرد بشكل ترفيهي وجميل
    caption = "🎨 **تم استلام صورتك بنجاح!**\n\nجاري معالجة الملامح وتحويلك إلى شخصية أنمي خرافية... 🪄✨\n\n*(هذه نسخة تجريبية سريعة لبوت الأنمي الخاص بك!)*"
    keyboard = [[InlineKeyboardButton("🔄 تجربة صورة أخرى", callback_data="convert_anime"), InlineKeyboardButton("🏠 الرئيسية", callback_data="main_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # نرد عليه بإحدى صور الأنمي كمثال للتحويل
    await update.message.reply_photo(photo=ANIME_IMAGES[1], caption=caption, reply_markup=reply_markup, parse_mode="Markdown")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    print("🌸 بوت الأنمي يعمل الآن بكفاءة...")
    app.run_polling()

if __name__ == "__main__":
    main()
