import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
HF_TOKEN = os.environ.get("HF_TOKEN")

# استخدام نموذج أنمي قوي وسريع ومخصص لتحويل الصور
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🌸 أنيمي ناعم", callback_data="style_soft"), InlineKeyboardButton("🔥 أنيمي أكشن", callback_data="style_action")],
        [InlineKeyboardButton("✨ أنيمي كلاسيكي", callback_data="style_classic"), InlineKeyboardButton("🖤 أنيمي مظلم", callback_data="style_dark")],
        [InlineKeyboardButton("👁️ أسلوب نينجا", callback_data="style_ninja"), InlineKeyboardButton("🐉 فانتازيا", callback_data="style_fantasy")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎨 **مرحباً بك في بوت تحويل الصور إلى أنمي!**\n\nاختر الأسلوب الذي تحبه من الأزرار أدناه، ثم أرسل صورتك لمعالجتها بالذكاء الاصطناعي ✨",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['selected_style'] = query.data
    
    style_names = {
        "style_soft": "🌸 أنيمي ناعم",
        "style_action": "🔥 أنيمي أكشن",
        "style_classic": "✨ أنيمي كلاسيكي",
        "style_dark": "🖤 أنيمي مظلم",
        "style_ninja": "👁️ أسلوب نينجا",
        "style_fantasy": "🐉 فانتازيا"
    }
    chosen_name = style_names.get(query.data, "أنيمي")
    await query.edit_message_text(text=f"✅ لقد اخترت: **{chosen_name}**\n\n📸 **أرسل صورتك الآن** لكي يبدأ الذكاء الاصطناعي بتطبيق هذا النمط عليها!", parse_mode="Markdown")

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_message = await update.message.reply_text("⏳ جاري تحويل صورتك إلى أنمي بالذكاء الاصطناعي...")
    
    try:
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        
        image_path = "temp_image.jpg"
        await file.download_to_drive(image_path)
        
        # قراءة الصورة وإرسالها مباشرة لـ API
        with open(image_path, "rb") as f:
            data = f.read()
            
        response = requests.post(API_URL, headers=headers, data=data, timeout=120)
        
        if response.status_code == 200:
            output_path = "output_anime.jpg"
            with open(output_path, "wb") as out_file:
                out_file.write(response.content)
                
            await update.message.reply_photo(photo=open(output_path, "rb"), caption="✨ تفضل صورتك بعد التحويل إلى أنمي!")
            os.remove(output_path)
        else:
            await update.message.reply_text(f"⚠️ النموذج مشغول حالياً (Code {response.status_code}). حاول مرة أخرى بعد قليل.")
            
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
