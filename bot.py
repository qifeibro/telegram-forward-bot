import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = int(os.environ.get("OWNER_ID"))

message_map = {}

async def handle_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.effective_message
    forwarded = await message.forward(chat_id=OWNER_ID)
    message_map[forwarded.message_id] = user.id
    await message.reply_text("✅ 你的消息已发送，我会尽快回复。")

async def handle_owner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    message = update.effective_message
    if not message.reply_to_message:
        await message.reply_text("⚠️ 请回复某条转发过来的消息。")
        return
    replied_id = message.reply_to_message.message_id
    if replied_id not in message_map:
        await message.reply_text("⚠️ 找不到对应用户。")
        return
    target_id = message_map[replied_id]
    if message.text:
        await context.bot.send_message(chat_id=target_id, text=message.text)
    elif message.photo:
        await context.bot.send_photo(chat_id=target_id, photo=message.photo[-1].file_id, caption=message.caption)
    elif message.document:
        await context.bot.send_document(chat_id=target_id, document=message.document.file_id, caption=message.caption)
    elif message.audio:
        await context.bot.send_audio(chat_id=target_id, audio=message.audio.file_id, caption=message.caption)
    elif message.voice:
        await context.bot.send_voice(chat_id=target_id, voice=message.voice.file_id, caption=message.caption)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_user))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_owner))
    app.run_polling()

if __name__ == "__main__":
    main()
