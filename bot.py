from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import BOT_TOKEN
import mcq_generator  # This must contain extract_mcqs(file_bytes) → returns list of MCQs

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\n📄 Please upload a PDF or Image file. I will extract MCQs and send them as plain text."
    )

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        file = update.message.document or update.message.photo[-1]
        telegram_file = await file.get_file()
        file_bytes = await telegram_file.download_as_bytearray()

        # MCQ extraction
        questions = mcq_generator.extract_mcqs(file_bytes)

        if not questions:
            await update.message.reply_text("⚠️ No MCQs found in the uploaded document.")
            return

        # Send extracted MCQs one by one
        for i, q in enumerate(questions, 1):
            text = f"Q{i}: {q['question']}\n"
            for idx, option in enumerate(q['options']):
                text += f"{chr(65+idx)}. {option}\n"
            text += f"\n✅ Answer: {chr(65 + q['answer'])}"
            await update.message.reply_text(text)

    except Exception as e:
        await update.message.reply_text(f"❌ Error processing file: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO, handle_document))
    app.run_polling()

if __name__ == "__main__":
    main()
