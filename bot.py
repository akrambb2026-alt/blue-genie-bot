import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

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
        "🎨 مرحباً بك في بوت تحويل الصور الفني!\n\nاختر الأسلوب الذي تفضله من الأزرار أعلاه، ثم أرسل صورتك ليقوم البوت بتعديلها وإرسالها فوراً ✨",
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
        context.user_data['selected_style'] = data
        await query.edit_message_text(
            text=f"✅ لقد اخترت الأسلوب: {name}\n\n📸 أرسل صورتك الآن في المحادثة لكي يقوم البوت بمعالجتها وإرسالها لك!",
            parse_mode="Markdown"
        )
    elif data == "menu_works":
        await query.edit_message_text(text="🖼️ سجل أعمالي السابقة فارغ حالياً.")
    elif data == "menu_stats":
        await query.edit_message_text(text="📊 إحصائياتك: 0 صور تم تحويلها حتى الآن.")
    elif data == "menu_features":
        await query.edit_message_text(text="💎 يتيح لك هذا البوت معالجة وتعديل صورك الشخصية لأنماط فنية رائعة بكل سهولة.")
    elif data == "menu_help":
        await query.edit_message_text(text="ℹ️ طريقة الاستخدام:\n1. اضغط على أحد الأنماط من الأزرار.\n2. أرسل صورتك مباشرة للمحادثة.\n3. انتظر ثوانٍ معدودة لتستلم صورتك المحولة.")

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_message = await update.message.reply_text("⏳ جاري معالجة وتعديل صورتك...")
    
    try:
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        
        image_path = "temp_image.jpg"
        output_path = "output_image.jpg"
        await file.download_to_drive(image_path)
        
        # معالجة الصورة محلياً بشكل مجاني بالكامل
        img = Image.open(image_path).convert("RGB")
        style = context.user_data.get('selected_style', 'style_soft')
        
        # تطبيق تأثيرات فنية بناء على اختيار المستخدم
        if style == 'style_action':
            img = ImageOps.posterize(img, 4)
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.8)
        elif style == 'style_dark':
            img = ImageOps.invert(img.convert('L')).convert('RGB')
            img = ImageOps.posterize(img, 3)
        elif style == 'style_classic':
            img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.5)
        else:
            img = img.filter(ImageFilter.SMOOTH_MORE)
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1.1)
            
        img.save(output_path)
        
        # إرسال الصورة الناتجة للمستخدم مباشرة
        with open(output_path, 'rb') as photo_file:
            await update.message.reply_photo(
                photo=photo_file,
                caption="✨ تم تحويل وتعديل صورتك بنجاح بواسطة البوت!"
            )
        
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
