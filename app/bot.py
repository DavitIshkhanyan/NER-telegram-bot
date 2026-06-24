import httpx
import sys
import os

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


async def handle_message(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):
    text = update.message.text

    # 1. Inform the user the bot is processing (good UX for slow APIs)
    await update.message.reply_chat_action("typing")

    try:
        # 2. Add an explicit timeout (e.g., 30 seconds for ML model predictions)
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                settings.api_url,
                json={"text": text}
            )
            # 3. Ensure we got a 200 OK before parsing JSON
            response.raise_for_status()

    except httpx.HTTPStatusError as e:
        await update.message.reply_text(f"API Error: Server responded with status {e.response.status_code}")
        return
    except httpx.RequestError:
        await update.message.reply_text("API Error: Could not connect to the prediction server.")
        return

    # 4. Safe parsing after validation
    data = response.json()
    entities = data.get("entities", [])

    if not entities:
        await update.message.reply_text("No entities found.")
        return

    # Your list comprehension string building is excellent and efficient
    result = "\n".join(
        f"{e['text']} → {e['label']}"
        for e in entities
    )

    await update.message.reply_text(result)


# Initialize application
app = Application.builder().token(settings.TELEGRAM_TOKEN).build()

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_message
    )
)

# Start the bot
app.run_polling()
