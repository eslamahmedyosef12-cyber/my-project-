from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# التوكن الخاص بك
TOKEN = '8987641718:AAFIvskZgSNNaW8wrmb6BSwnxrDa7iKEjkk'

# قائمة مهام بسيطة في الذاكرة (مؤقتة)
tasks = []

# 1. إضافة مهمة
async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    task = " ".join(context.args)
    if not task:
        await update.message.reply_text("اكتب المهمة بعد الأمر يا بطل. مثال: /add مذاكرة فيزياء")
        return
    tasks.append(task)
    await update.message.reply_text(f"تمت إضافة المهمة لجدول HAMO ABO KALAS: {task}")

# 2. عرض المهام
async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not tasks:
        await update.message.reply_text("جدولك فاضي يا بطل، استمتع بوقتك!")
        return
    
    msg = "📋 **جدول أعمال HAMO ABO KALAS:**\n\n"
    for i, t in enumerate(tasks, 1):
        msg += f"{i}. {t}\n"
    await update.message.reply_text(msg, parse_mode='Markdown')

# 3. حذف مهام
async def clear_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks.clear()
    await update.message.reply_text("تم مسح الجدول بنجاح.. ابدأ من جديد يا بطل!")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("add", add_task))
    app.add_handler(CommandHandler("list", list_tasks))
    app.add_handler(CommandHandler("clear", clear_tasks))
    
    print("بوت تنظيم الوقت لـ HAMO ABO KALAS يعمل...")
    app.run_polling()

