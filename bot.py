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
        "🎨 مرحباً بك في بوت معالجة وتعديل الصور!\n\nاختر الأسلوب الذي تفضله من الأزرار أعلاه، ثم أرسل صورتك لتتم معالجتها فوراً ✨",
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
        context.user_data['style_name'] = name
        await query.edit_message_text(
            text=f"✅ لقد اخترت الأسلوب: {name}\n\n📸 أرسل صورتك الآن في المحادثة لكي يقوم البوت بمعالجتها وإرسالها لك!",
            parse_mode="Markdown"
        )
    elif data == "menu_works":
        await query.edit_message_text(text="🖼️ سجل أعمالي السابقة فارغ حالياً.")
    elif data == "menu_stats":
        await query.edit_message_text(text="📊 إحصائياتك: 0 صور تم تحويلها حتى الآن.")
    elif data == "menu_features":
        await query.edit_message_text(text="💎 يتيح لك هذا البوت معالجة صورك الشخصية لأنماط فنية مميزة بكل سرعة.")
    elif data == "menu_help":
        await query.edit_message_text(text="ℹ️ طريقة الاستخدام:\n1. اضغط على أحد الأنماط من الأزرار.\n2. أرسل صورتك مباشرة للمحادثة.\n3. استلم صورتك المعدلة فوراً.")

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_message = await update.message.reply_text("⏳ جاري معالجة صورتك...")
    
    try:
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        
        image_path = "temp_input.jpg"
        output_path = "temp_output.jpg"
        await file.download_to_drive(image_path)
        
        img = Image.open(image_path).convert("RGB")
        style = context.user_data.get('selected_style', 'style_soft')
        style_name = context.user_data.get('style_name', 'أنيمي ناعم')
        
        # تعديلات وتأثيرات فنية متقدمة ومضبوطة بعناية
        if style == 'style_action' or style == 'style_ninja':
            # تباين قوي وإبراز الحواف لتعطاء طابع أكشن وحاد
            img = img.filter(ImageFilter.FIND_EDGES)
            img = ImageOps.invert(img)
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(2.0)
        elif style == 'style_dark':
            # نمط مظلم وسينمائي
            img = ImageOps.grayscale(img)
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.8).convert("RGB")
        elif style == 'style_classic' or style == 'style_fantasy':
            # إبراز تفاصيل كلاسيكية ونقاء عالٍ
            img = img.filter(ImageFilter.DETAIL)
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.4)
        else:
            # نمط ناعم
            img = img.filter(ImageFilter.SMOOTH)
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1.05)
            
        img.save(output_path)
        
        with open(output_path, 'rb') as photo_file:
            await update.message.reply_photo(
                photo=photo_file,
                caption=f"✨ تم تعديل صورتك بنجاح بنمط ({style_name})!"
            )
        
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
