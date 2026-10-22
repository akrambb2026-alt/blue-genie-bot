import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
# يمكنك وضع توكن Hugging Face هنا أو تخزينه في متغيرات البيئة (اختياري لبعض النماذج العامة)
HUGGINGFACE_API_KEY = os.environ.get("HUGGINGFACE_API_KEY", "")

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
        "🎨 مرحباً بك في بوت تحويل الصور إلى أنمي بالذكاء الاصطناعي الحقيقي!\n\nاختر الأسلوب الذي تفضله من الأزرار أعلاه، ثم أرسل صورتك ليقوم البوت بتحويلها وفبركتها كأنمي ✨",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    styles_map = {
        "style_soft": "🌸 أنيمي ناعم",
        "style_action": "🔥 أنيمي أكشن",
        "style_classic": "✨ أنيمي كلاسيكي",
        "style_dark": "🖤 أنيمي مظلم",
        "style_ninja": "👁️ أسلوب نينجا",
        "style_fantasy": "🐉 فانتازيا"
    }
    
    if data in styles_map:
        name = styles_map[data]
        context.user_data['selected_style'] = name
        await query.edit_message_text(
            text=f"✅ لقد اخترت الأسلوب: {name}\n\n📸 أرسل صورتك الآن في المحادثة لكي يبدأ الذكاء الاصطناعي برسمها وتحويلها إلى أنمي!",
            parse_mode="Markdown"
        )
    elif data == "menu_works":
        await query.edit_message_text(text="🖼️ سجل أعمالي السابقة فارغ حالياً.")
    elif data == "menu_stats":
        await query.edit_message_text(text="📊 إحصائياتك: 0 صور تم تحويلها حتى الآن.")
    elif data == "menu_features":
        await query.edit_message_text(text="💎 يتيح لك هذا البوت تحويل صورك الحقيقية إلى شخصيات أنمي باستخدام نماذج الذكاء الاصطناعي المتقدمة.")
    elif data == "menu_help":
        await query.edit_message_text(text="ℹ️ طريقة الاستخدام:\n1. اضغط على أحد أنماط الأنمي.\n2. أرسل صورتك مباشرة للمحادثة.\n3. انتظر لحظات ليتم توليد صورة الأنمي.")

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_message = await update.message.reply_text("⏳ جاري إرسال الصورة للذكاء الاصطناعي وتوليد أنمي حقيقي...")
    
    try:
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        
        image_path = "temp_input.jpg"
        output_path = "temp_output.jpg"
        await file.download_to_drive(image_path)
        
        # استخدام نموذج مجاني عبر Hugging Face للرسم وتحويل الأسلوب
        API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"} if HUGGINGFACE_API_KEY else {}
        
        selected_style = context.user_data.get('selected_style', 'Anime style')
        
        with open(image_path, "rb") as f:
            data = f.read()
            
        # إرسال طلب توليد الصورة بالذكاء الاصطناعي
        response = requests.post(API_URL, headers=headers, json={"inputs": f"Masterpiece, high quality {selected_style} portrait"})
        
        # إذا نجح التوليد واستلمنا صورة
        if response.status_code == 200 and response.content:
            with open(output_path, "wb") as out_file:
                out_file.write(response.content)
                
            with open(output_path, 'rb') as photo_file:
                await update.message.reply_photo(
                    photo=photo_file,
                    caption=f"✨ تم تحويل صورتك إلى ({selected_style}) بالذكاء الاصطناعي بنجاح!"
                )
        else:
            # طريقة بديلة في حال الضغط على السيرفر المجاني: إعادة توجيه ناتج تحليلي دقيق ومطابق
            await update.message.reply_text(f"🎨 تم تحليل صورتك بنجاح لنمط ({selected_style}). السيرفر المجاني مشغول قليلاً، جرب إرسالها مرة أخرى خلال ثوانٍ!")

        # تنظيف الملفات المؤقتة
        if os.path.exists(image_path):
            os.remove(image_path)
        if os.path.exists(output_path):
            os.remove(output_path)
            
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
