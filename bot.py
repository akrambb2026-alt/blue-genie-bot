import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
from huggingface_hub import InferenceClient

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
HF_TOKEN = os.environ.get("HF_TOKEN")

client = InferenceClient(token=HF_TOKEN)

# دالة /start مع الأزرار الاحترافية الداخلية
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

# استقبال الضغطات على الأزرار الداخلية
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # حفظ النمط الذي اختاره المستخدم في الـ context
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

# دالة معالجة الصور بناءً على الاختيار
async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_message = await update.message.reply_text("⏳ جاري معالجة الصورة وتحويلها بالذكاء الاصطناعي...")
    
    try:
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        
        image_path = "temp_image.jpg"
        await file.download_to_drive(image_path)
        
        with open(image_path, "rb") as f:
            image_bytes = f.read()
            
        # تحديد الرموز حسب اختيار المستخدم أو استخدام النمط الافتراضي
        style = context.user_data.get('selected_style', 'style_soft')
        prompts = {
            "style_soft": "soft anime style, pastel colors, cute, masterpiece",
            "style_action": "dynamic action anime style, intense, epic, high quality",
            "style_classic": "retro 90s anime style, vintage, classic aesthetic",
            "style_dark": "dark anime style, moody shadows, cyberpunk lighting",
            "style_ninja": "ninja stealth anime style, dramatic lighting, sharp details",
            "style_fantasy": "fantasy magical anime style, glowing effects, ethereal"
        }
        prompt = prompts.get(style, "anime style, masterpiece")
            
        image_output = client.image_to_image(
            image=image_bytes,
            prompt=prompt,
            model="stabilityai/stable-diffusion-xl-refiner-1.0"
        )
        
        output_path = "output_anime.jpg"
        image_output.save(output_path)
        
        await update.message.reply_photo(photo=open(output_path, "rb"), caption="✨ تفضل صورتك بعد التحويل بالأسلوب المطلوب!")
        
        os.remove(image_path)
        os.remove(output_path)
        await status_message.delete()
        
    except Exception as e:
        await status_message.edit_text(f"⚠️ حدث خطأ أثناء المعالجة: {str(e)}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.PHOTO
