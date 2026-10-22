import os
import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
HF_TOKEN = os.environ.get("HF_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

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

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    styles_map = {
        "🌸 أنيمي ناعم": "soft anime style, pastel colors, cute, masterpiece",
        "🔥 أنيمي أكشن": "dynamic action anime style, intense, epic, high quality",
        "✨ أنيمي كلاسيكي": "retro 90s anime style, vintage, classic aesthetic",
        "🖤 أنيمي مظلم": "dark anime style, moody shadows, cyberpunk lighting",
        "👁️ أسلوب نينجا": "ninja stealth anime style, dramatic lighting, sharp details",
        "🐉 فانتازيا": "fantasy magical anime style, glowing effects, ethereal"
    }
    
    if text in styles_map:
        context.user_data['selected_style'] = text
        context.user_data['selected_prompt'] = styles_map[text]
        await update.message.reply_text(f"✅ لقد اخترت الأسلوب: **{text}**\n\n📸 **أرسل صورتك الآن** في المحادثة لكي يبدأ الذكاء الاصطناعي بتطبيق هذا النمط عليها!", parse_mode="Markdown")
    
    elif text == "🖼️ أعمالي السابقة":
        await update.message.reply_text("🖼️ سجل أعمالك السابقة فارغ حالياً.")
    elif text == "📊 إحصائياتي":
        await update.message.reply_text("📊 إحصائياتك: 0 صور تم تحويلها حتى الآن.")
    elif text == "💎 المميزات":
        await update.message.reply_text("💎 يتيح لك هذا البوت تحويل صورك الشخصية إلى رسومات أنمي احترافية ومتعددة الأنماط بكل سهولة.")
    elif text == "ℹ️ المساعدة":
        await update.message.reply_text("ℹ️ طريقة الاستخدام:\n1. اضغط على أحد أنماط الأنمي من الأزرار بالأسفل.\n2. أرسل صورتك مباشرة.\n3. انتظر ثوانٍ معدودة لتستلم صورتك المحولة.")
    elif text == "👑 المطور":
        dev_link = "https://www.facebook.com/profile.php?id=61594929560699"
        await update.message.reply_text(f"👑 **المطور:**\nيمكنك التواصل مع المطور عبر الرابط التالي:\n{dev_link}", parse_mode="Markdown")
    else:
        await update.message.reply_text("يرجى اختيار أحد الأزرار الموجودة بالأسفل أو إرسال صورة للبدء.")

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_message = await update.message.reply_text("⏳ جاري تحويل صورتك إلى أنمي بالذكاء الاصطناعي...")
    
    try:
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        
        image_path = "temp_image.jpg"
        await file.download_to_drive(image_path)
        
        with open(image_path, "rb") as f:
            data = f.read()
            
        prompt = context.user_data.get('selected_prompt', "soft anime style, pastel colors, cute, masterpiece")
            
        response = requests.post(API_URL, headers=headers, data=data, timeout=120)
        
        if response.status_code == 200:
            output_path = "output_anime.jpg"
            with open(output_path, "wb") as out_file:
                out_file.write(response.content)
                
            await update.message.reply_photo(photo=open(output_path, "rb"), caption="✨ تفضل صورتك بعد التحويل إلى أنمي!")
            os.remove(output_path)
        else:
            await update.message.reply_text(f"⚠️ النموذج يتم تحميله حالياً (Code {response.status_code}). حاول إرسال الصورة مرة أخرى بعد لحظات.")
            
        os.remove(image_path)
        await status_message.delete()
        
    except requests.exceptions.RequestException:
        await status_message.edit_text("⚠️ حدث خطأ في الاتصال بالشبكة. يرجى المحاولة مرة أخرى بعد قليل.")
    except Exception as e:
        await status_message.edit_text(f"⚠️ حدث خطأ أثناء المعالجة: {str(e)}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_handler(MessageHandler(filters.PHOTO, handle_image))
    
    print("Bot is running...")
    application.run_polling()
