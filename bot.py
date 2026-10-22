import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from huggingface_hub import InferenceClient

# قراءة المفاتيح بأمان من متغيرات البيئة في Render
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
HF_TOKEN = os.environ.get("HF_TOKEN")

# إعداد عميل Hugging Face (باستخدام نموذج تحويل الصور الشهير)
client = InferenceClient(token=HF_TOKEN)

# دالة بدء التشغيل وعرض الأزرار
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🌸 أنيمي ناعم", "🔥 أنيمي أكشن"],
        ["✨ أنيمي كلاسيكي", "🖤 أنيمي مظلم"],
        ["👁️ أسلوب نينجا", "🐉 فانتازيا"],
        ["🖼️ أعمالي السابقة", "📊 إحصائياتي"],
        ["💎 المميزات", "ℹ️ المساعدة"],
        ["👑 المطور"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "📸 **أرسل صورتك الآن في المحادثة** لكي يبدأ الذكاء الاصطناعي بتحويلها للأسلوب الذي تناسبه! ✨",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# دالة استقبال ومعالجة الصور
async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # إعلام المستخدم بأن العمل جاري
    status_message = await update.message.reply_text("⏳ جاري معالجة الصورة وتحويلها بالذكاء الاصطناعي...")
    
    try:
        # الحصول على أعلى جودة للصورة المرسلة
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        
        # تحميل الصورة مؤقتاً
        image_path = "temp_image.jpg"
        await file.download_to_drive(image_path)
        
        # قراءة الصورة وإرسالها لنموذج Hugging Face
        with open(image_path, "rb") as f:
            image_bytes = f.read()
            
        # استخدام نموذج توليد/تحويل الصور (يمكنك تغيير اسم النموذج حسب رغبتك)
        image_output = client.image_to_image(
            image=image_bytes,
            prompt="anime style, masterpiece, high quality, vibrant colors",
            model="stabilityai/stable-diffusion-xl-refiner-1.0" # نموذج افتراضي قوي
        )
        
        # حفظ الصورة الناتجة
        output_path = "output_anime.jpg"
        image_output.save(output_path)
        
        # إرسال الصورة الناتجة للمستخدم
        await update.message.reply_photo(photo=open(output_path, "rb"), caption="✨ تفضل صورتك بعد التحويل إلى أنمي!")
        
        # حذف الملفات المؤقتة
        os.remove(image_path)
        os.remove(output_path)
        await status_message.delete()
        
    except Exception as e:
        await status_message.edit_text(f"⚠️ حدث خطأ أثناء المعالجة: {str(e)}")

if __name__ == '__main__':
    # بناء وتكييف تطبيق تليجرام
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # إضافة المعالجات (Handlers)
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_image))
    
    # تشغيل البوت
    print("Bot is running...")
    application.run_polling()
