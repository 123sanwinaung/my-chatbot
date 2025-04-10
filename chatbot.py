from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

queue = []
pairs = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    if user_id in pairs:
        await update.message.reply_text("📢 You're already chatting.")
        return
    if queue:
        partner_id = queue.pop(0)
        pairs[user_id] = partner_id
        pairs[partner_id] = user_id
        await context.bot.send_message(partner_id, "✅ Connected to a new partner!")
        await update.message.reply_text("✅ Connected to a new partner!")
    else:
        queue.append(user_id)
        await update.message.reply_text("⏳ Waiting for a partner...")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    if user_id in pairs:
        partner_id = pairs[user_id]
        del pairs[partner_id]
        del pairs[user_id]
        await context.bot.send_message(partner_id, "❌ Your partner has left the chat.")
        await update.message.reply_text("❌ You have left the chat.")
    elif user_id in queue:
        queue.remove(user_id)
        await update.message.reply_text("⛔ You left the waiting queue.")
    else:
        await update.message.reply_text("⚠️ You're not in a chat or queue.")

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    if user_id in pairs:
        partner_id = pairs[user_id]
        await context.bot.send_message(partner_id, update.message.text)

app = ApplicationBuilder().token("8074695579:AAGU1Aen9rl-ZzJ8sp2H78nwJPC_ClXE_ps").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stop", stop))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

app.run_polling()
