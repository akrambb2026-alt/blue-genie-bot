import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
from huggingface_hub import InferenceClient

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
HF_TOKEN = os.environ.get("HF_TOKEN")

client = InferenceClient(token=HF_TOKEN, timeout=120)

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
        "🎨 **مرحباً بك في بوت تحويل الصور إلى أنمي!**\n\nاختر الأسلوب الذي تفضله من الأزرار أعلاه، ثم أرسل صورتك لمعالجتها بالذكاء الاصطناعي ✨",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    styles_map = {
        "style_soft": ("🌸 أنيمي ناعم", "soft anime style, pastel colors, cute, masterpiece"),
        "style_action": ("🔥 أنيمي أكشن", "dynamic action anime style, intense, epic, high quality"),
        "style_classic": ("✨ أنيمي كلاسيكي", "retro 90s anime style, vintage, classic aesthetic"),
        "style_dark": ("🖤 أنيمي مظلم", "dark anime style, moody shadows, cyberpunk lighting"),
        "style_ninja": ("👁️ أسلوب نينجا", "ninja stealth anime style, dramatic lighting, sharp details"),
        "style_fantasy": ("🐉 فانتازيا", "fantasy magical anime style, glowing effects, ethereal")
    }
    
    if data in styles_map:
        name, prompt = styles_map[data]
        context.user_data['selected_style'] = name
        context.user_data['selected_prompt'] = prompt
        await query.edit_message_text(
            text=f"✅ لقد اخترت الأسلوب: **{name}**\n\n📸 **أرسل صورتك الآن** في المحادثة لكي يبدأ الذكاء الاصطناعي بتطبيق هذا النمط عليها!",
            parse_mode="Markdown"
        )
    elif data == "menu_works":
        await query.edit_message_text(text="🖼️ سجل أعمالك السابقة فارغ حالياً.")
    elif data == "menu_stats":
        await query.edit_message_text(text="📊 إحصائياتك: 0 صور تم تحويلها حتى الآن.")
    elif data == "menu_features":
        await query.edit_message_text(text="💎 يتيح لك هذا البوت تحويل صورك الشخصية إلى رسومات أنمي احترافية ومتعددة الأ
