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
        "style_soft": ("🌸 أنيمي ناعم", "Transform this image into a cute soft anime art style, masterpiece."),
        "style_action": ("🔥 أنيمي أكشن", "Transform this image into a dynamic action anime style, epic, high quality."),
        "style_classic": ("✨ أنيمي كلاسيكي", "Transform this image into a retro 90s classic anime style."),
        "style_dark": ("🖤 أنيمي مظلم", "Transform this image into a dark cyberpunk anime style with moody shadows."),
        "style_ninja": ("👁️ أسلوب نينجا", "Transform this image into a ninja stealth anime style with dramatic lighting."),
        "style_fantasy": ("🐉 فانتازيا", "Transform this image into a fantasy magical anime style with glowing effects.")
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
        
        img = Image.open(image_path)
        prompt = context.user_data.get('selected_prompt', "Transform this image into a cute soft anime art style.")
        
        model = genai.GenerativeModel('gemini-3.8-flash')
        response = model.generate_content([prompt, img])
        
        await update.message.reply_text(f"✨ النتيجة ووصف التحويل:\n{response.text}")
        
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
