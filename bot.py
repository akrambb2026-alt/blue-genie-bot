import os
import logging
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

TOKEN = os.environ.get("TELEGRAM_TOKEN")

ANIME_IMAGES = [
    "https://images.unsplash.com/photo-1578632767115-351597cf2477?w=600",
    "https://images.unsplash.com/photo-1563089145-599997674d42?w=600"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎨 تحويل إلى أنمي", callback_data="main_convert")],
        [
            InlineKeyboardButton("🔥 أنمي أكشن", callback_data="style_action"),
            InlineKeyboardButton("🌸 أنمي ناعم", callback_data="style_soft")
        ],
        [
            InlineKeyboardButton("🖤 أنمي مظلم", callback_data="style_dark"),
            InlineKeyboardButton("✨ أنمي كلاسيكي", callback_data="style_classic")
        ],
        [
            InlineKeyboardButton("👁️ أسلوب نينجا", callback_data="style_ninja"),
            InlineKeyboardButton("🐉 فانتازيا", callback_data="style_fantasy")
        ],
        [
            InlineKeyboardButton("🖼️ أعمالي السابقة", callback_data="my_works"),
            InlineKeyboardButton("📊 إحصائياتي", callback_data="my_stats")
        ],
        [
            InlineKeyboardButton("💎 المميزات", callback_data="features"),
            InlineKeyboardButton("ℹ️ المساعدة", callback_data="help")
        ],
        [InlineKeyboardButton("👑 المطور", callback_data="developer")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = (
        "┌  ⌜ 🗡️  ANIME AI ⌟  ┐\n\n"
        "┃  ⚡ | مرحبًا بك في عالم الأنمي!\n\n"
        "🎨 | حوّل صورك إلى شخصيات أنمي مذهلة.\n"
        "🔥 | اكتشف
