import os
import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
HF_TOKEN = os.environ.get("HF_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# دالة بدء التشغيل وعرض الأزرار بالأسفل
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🔥 أنيمي أكشن", "🌸 أنيمي ناعم"],
        ["🖤 أنيمي مظلم", "✨ أنيمي كلاسيكي"],
        ["👁️ أسلوب نينجا", "🐉 فانتازيا"],
        ["🖼️ أعمالي السابقة", "📊 إحصائياتي"],
        ["💎 المميزات", "ℹ️ المساعدة"],
        ["👑 المطور"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "🎨 **مرحباً بك في بوت تحويل الصور إلى أنمي!**\n\nاختر الأسلوب الذي تفضله من الأزرار بالأسفل، ثم أرسل صورتك لمعالجتها بالذكاء الاصطناعي ✨",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# دالة معالجة الأزرار والنصوص
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    styles_map = {
        "🌸 أنيمي ناعم": "soft anime style, pastel colors, cute, masterpiece",
        "🔥 أنيمي أكشن": "dynamic action
