import os
import google.generativeai as genai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
from PIL import Image

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🔥 أنيمي أكشن", callback_data="style_action"),
            InlineKeyboardButton("🌸 أنيمي ناعم", callback_data="style_soft")
        ],
        [
            InlineKeyboardButton("🖤 أنيمي مظلم", callback_data="style_dark"),
            InlineKeyboardButton("✨ أنيمي كلاسيكي", callback_data="style_classic")
        ],
        [
            InlineKeyboardButton("👁️ أسلوب نينجا", callback_data="style_ninja"),
            InlineKeyboardButton("🐉 فانتازيا", callback_data="style_fantasy")
        ],
        [
            InlineKeyboardButton("🖼️ أعمالي السابقة", callback_data="menu_works"),
            InlineKeyboardButton("📊 إحصائياتي", callback_data="menu_stats")
        ],
        [
            InlineKeyboardButton("💎 المميزات", callback_data="menu_features"),
            InlineKeyboardButton("ℹ️ المساعدة", callback_data="menu_help")
        ],
        [
            InlineKeyboardButton("👑 المطور", url="https://www.facebook.com/profile.php?id=61594929560699")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎨 مرحباً بك في بوت تحويل الصور إلى أنمي!\n\nاختر الأسلوب الذي تفضله من الأزرار أعلاه، ثم أرسل صورتك لمعالجتها بالذكاء الاصطناعي ✨",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    styles_map = {
        "
