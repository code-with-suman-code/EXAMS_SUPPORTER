from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from config import BOT_TOKEN
import mcq_generator

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to EXAMS_SUPPORTER Bot!\n\n"
        "📄 Please upload a PDF or Image file containing educational notes.\n"
        "The bot will extract MCQs and quiz you interactively."
    )

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document or update.message.photo[-1]
    file_path = await file.get_file()
    file_bytes = await file_path.download_as_bytearray()
    questions = mcq_generator.extract_mcqs(file_bytes)
    context.user_data['questions'] = questions
    context.user_data['q_index'] = 0
    await send_question(update, context)

async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    index = context.user_data['q_index']
    questions = context.user_data['questions']
    if index >= len(questions):
        await update.message.reply_text("✅ Quiz complete!")
        return
    q = questions[index]
    buttons = [[InlineKeyboardButton(opt, callback_data=str(i))] for i, opt in enumerate(q['options'])]
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(f"Q{index+1}: {q['question']}", reply_markup=reply_markup)

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    index = context.user_data['q_index']
    q = context.user_data['questions'][index]
    selected = int(query.data)
    correct = q['answer']
    response = "✅ Correct!" if selected == correct else f"❌ Wrong! Correct answer: {q['options'][correct]}"
    await query.edit_message_text(response)
    context.user_data['q_index'] += 1
    await send_question(update, context)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO, handle_document))
    app.add_handler(CallbackQueryHandler(handle_answer))
    app.run_polling()

if __name__ == "__main__":
    main()
  
