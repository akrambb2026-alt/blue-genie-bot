import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
HF_TOKEN = os.environ.get("HF_TOKEN")

# نموذج أنمي قوي وموثوق للتحويل المباشر
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

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
            text=f"✅ لقد اخترت الأسلوب: {name}\n\n📸 أرسل صورتك الآن في المحادثة لكي يبدأ الذكاء الاصطناعي بتطبيق هذا النمط عليها!",
            parse_mode="Markdown"
        )
    elif data == "menu_works":
        await query.edit_message_text(text="🖼️ سجل أعمالي السابقة فارغ حالياً.")
    elif data == "menu_stats":
        await query.edit_message_text(text="📊 إحصائياتك: 0 صور تم تحويلها حتى الآن.")
    elif data == "menu_features":
        await query.edit_message_text(text="💎 يتيح لك هذا البوت تحويل صورك الشخصية إلى رسومات أنمي احترافية ومتعددة الأنماط بكل سهولة.")
    elif data == "menu_help":
        await query.edit_message_text(text="ℹ️ طريقة الاستخدام:\n1. اضغط على أحد أنماط الأنمي من الأزرار.\n2. أرسل صورتك مباشرة للمحادثة.\n3. انتظر ثوانٍ معدودة لتستلم صورتك المحولة.")

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_message = await update.message.reply_text("⏳ جاري تحويل صورتك إلى أنمي بالذكاء الاصطناعي...")
    
    try:
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        
        image_path = "temp_image.jpg"
        await file.download_to_drive(image_path)
        
        with open(image_path, "rb") as f:
            data = f.read()
            
        # إرسال الصورة مباشرة للنموذج عبر requests
        response = requests.post(API_URL, headers=headers, data=data, timeout=120)
        
        if response.status_code == 200:
            output_path = "output_anime.jpg"
            with open(output_path, "wb") as out_file:
                out_file.write(response.content)
                
            await update.message.reply_photo(photo=open(output_path, "rb"), caption="✨ تفضل صورتك بعد التحويل إلى أنمي!")
            os.remove(output_path)
        else:
            await update.message.reply_text(f"⚠️ النموذج مشغول حالياً (Code {response.status_code}). حاول إرسال الصورة مرة أخرى بعد قليل.")
            
        os.remove(image_path)
        await status_message.delete()
        
    except Exception as e:
        await status_message.edit_text(f"⚠️ حدث خطأ أثناء المعالجة: {str(e)}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.PHOTO, handle_image))
    
    print("Bot is running...")
    application.run_polling()
