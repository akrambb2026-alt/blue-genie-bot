import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
from huggingface_hub import InferenceClient

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
HF_TOKEN = os.environ.get("HF_TOKEN")

client = InferenceClient(token=HF_TOKEN, timeout=120)

# دالة بدء التشغيل مع الأزرار التفاعلية الداخلية (Inline Keyboard) تحت الرسالة
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔥 أنيمي أكشن", callback_data="style_action"), InlineKeyboardButton("🌸 أنيمي ناعم", callback_data="style_soft")],
        [InlineKeyboardButton("🖤 أنيمي مظلم", callback_data="style_dark"), InlineKeyboardButton("✨ أنيمي كلاسيكي", callback_data="style_classic")],
        [InlineKeyboardButton("👁️ أسلوب نينجا", callback_data="style_ninja"), InlineKeyboardButton("🐉 فانتازيا", callback_data="style_fantasy")],
        [InlineKeyboardButton("🖼️ أعمالي السابقة", callback_data="menu_works"), InlineKeyboardButton("📊 إحصائياتي", callback_data="menu_stats")],
        [InlineKeyboardButton("💎 المميزات", callback_data="menu_features"), InlineKeyboardButton
