import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import httpx

# إعداد السجلات لمتابعة حالة البوت
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# جلب التوكنات من متغيرات البيئة في Render
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")

# نموذج الذكاء الاصطناعي لتحويل الصور (مثال: Stable Diffusion)
HF_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # التأكد من أن المستخدم أرسل صورة
    if not update.message.photo:
        await update.message.reply_text("الرجاء إرسال صورة وسأقوم بتحويلها لك بالذكاء الاصطناعي! 🎨")
        return

    # إعلام المستخدم أن البوت جاري العمل على الصورة
    processing_message = await update.message.reply_text("⏳ جاري معالجة الصورة وتحويلها بواسطة الذكاء الاصطناعي، انتظر قليلاً...")

    try:
        # الحصول على أعلى دقة للصورة المرتسلة
        photo_file = await update.message.photo[-1].get_file()
        image_bytes = await photo_file.download_as_bytearray()

        # إرسال الصورة إلى واجهة برمجة تطبيقات Hugging Face
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                HF_API_URL,
                headers=headers,
                content=image_bytes
            )

        # التحقق من نجاح العملية
        if response.status_code == 200:
            output_image_bytes = response.content
            # حذف رسالة الانتظار
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=processing_message.message_id)
            # إرسال الصورة الناتجة للمستخدم
            await update.message.reply_photo(photo=output_image_bytes, caption="✨ تم تحويل الصورة بنجاح بواسطة الذكاء الاصطناعي!")
        else:
            logger.error(f"Hugging Face API Error: {response.status_code} - {response.text}")
            await context.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=processing_message.message_id,
                text="⚠️ عذراً، حدث خطأ أثناء معالجة الصورة عبر نموذج الذكاء الاصطناعي. حاول مرة أخرى لاحقاً."
            )

    except Exception as e:
        logger.error(f"Error processing image: {e}")
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=processing_message.message_id,
            text="⚠️ حدث خطأ غير متوقع أثناء الاتصال بالخادم."
        )

def main():
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN is missing!")
        return

    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # معالجة الصور المرسلة
    application.add_handler(MessageHandler(filters.PHOTO, handle_image))

    logger.info("Bot is starting...")
    application.run_polling()

if __name__ == "__main__":
    main()
