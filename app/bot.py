import httpx
import sys
import os
from gradio_client import Client

# Your path fix works perfectly for absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .settings import settings
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters
)

client = Client("DavitIshkhanyan/NeuraNER")

# async def handle_message(
#         update: Update,
#         context: ContextTypes.DEFAULT_TYPE
# ):
#     text = update.message.text
#
#     # 1. Inform the user the bot is processing (good UX for slow APIs)
#     await update.message.reply_chat_action("typing")
#
#     try:
#         # 2. Add an explicit timeout (e.g., 30 seconds for ML model predictions)
#         async with httpx.AsyncClient(timeout=30.0) as client:
#             response = await client.post(
#                 settings.api_url,
#                 json={"text": text}
#             )
#             # 3. Ensure we got a 200 OK before parsing JSON
#             response.raise_for_status()
#
#     except httpx.HTTPStatusError as e:
#         await update.message.reply_text(f"API Error: Server responded with status {e.response.status_code}")
#         return
#     except httpx.RequestError:
#         await update.message.reply_text("API Error: Could not connect to the prediction server.")
#         return
#
#     # 4. Safe parsing after validation
#     data = response.json()
#     entities = data.get("entities", [])
#
#     if not entities:
#         await update.message.reply_text("No entities found.")
#         return
#
#     # Your list comprehension string building is excellent and efficient
#     result = "\n".join(
#         f"{e['text']} → {e['label']}"
#         for e in entities
#     )
#
#     await update.message.reply_text(result)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_chat_action("typing")

    try:
        # Call the Space API directly
        result = client.predict(text=text, api_name="/predict")
    except Exception as e:
        await update.message.reply_text(f"API Error: {e}")
        return

    if not result:
        await update.message.reply_text("No entities found.")
        return

    # Format the list of entities nicely
    formatted = "\n".join(
        f"{e['text']} → {e['label']} ({e['score']})"
        for e in result
    )
    await update.message.reply_text(formatted)

# Initialize application
app = Application.builder().token(settings.TELEGRAM_TOKEN).build()

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_message
    )
)

# Start the bot
# app.run_polling()
app.run_webhook(
    listen="0.0.0.0",
    port=int(os.environ.get("PORT", 7860)),  # Render expects PORT
    url_path=settings.TELEGRAM_TOKEN,
    webhook_url=f"https://{settings.RENDER_URL}/{settings.TELEGRAM_TOKEN}"
)