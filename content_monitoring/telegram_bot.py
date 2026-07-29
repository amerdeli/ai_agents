# content_monitoring/telegram_bot.py
import os
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)
from content_monitoring.main import run_pipeline

load_dotenv()

BOT_TOKEN = os.getenv("CONTENT_MONITOR_BOT_TOKEN")
CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID"))


def is_authorised(update: Update) -> bool:
    """
    Security check — only allow messages from my chat ID.
    """
    return update.effective_chat.id == CHAT_ID


# Commands

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for /start command"""
    if not is_authorised(update):
        await update.message.reply_text("⛔ Unauthorised!")
        return

    await update.message.reply_text(
        "Hey there👋! Ready to check for new content?"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for /help command"""
    if not is_authorised(update):
        await update.message.reply_text("⛔ Unauthorised!")
        return

    await update.message.reply_text(
        "🤖 Content Monitor Bot commands:\n\n"
        "/check  — check news and YouTube for new content\n"
        "/status — show last digest summary\n"
        "/clear  — reset seen content lists\n"
        "/help   — show this message"
    )


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for /check command — triggers full content monitoring pipeline"""
    if not is_authorised(update):
        await update.message.reply_text("⛔ Unauthorised!")
        return

    await update.message.reply_text("🚀 Content check starting — this may take a minute...")

    try:
        # Run the pipeline — returns path to digest file
        digest_path = run_pipeline()

        if digest_path is None:
            await update.message.reply_text(
                "⚠️ Pipeline completed but no new content found today!"
            )
            return

        # Read the digest file
        with open(digest_path, "r", encoding="utf-8") as f:
            digest_content = f.read()

        # Split digest into chunks if needed (4096 character limit per message)
        if len(digest_content) <= 4096:
            await update.message.reply_text(digest_content)
        else:
            chunks = [
                digest_content[i:i+4096]
                for i in range(0, len(digest_content), 4096)
            ]
            for chunk in chunks:
                await update.message.reply_text(chunk)

    except Exception as e:
        await update.message.reply_text(f"❌ Pipeline failed: {str(e)}")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for /status — shows most recent digest summary"""
    if not is_authorised(update):
        await update.message.reply_text("⛔ Unauthorised!")
        return

    from content_monitoring.config import DIGESTS_DIR

    # Find the most recent digest file
    digests = sorted(DIGESTS_DIR.glob("digest_*.md"), reverse=True)

    if not digests:
        await update.message.reply_text("📭 No digests found yet — run /check first!")
        return

    latest_digest = digests[0]
    date_str = latest_digest.stem.replace("digest_", "").replace("_", "-")

    await update.message.reply_text(
        f"📊 Latest digest: {date_str}\n"
        f"📁 File: {latest_digest.name}\n\n"
        f"Run /check to generate a fresh digest!"
    )


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for /clear — resets seen articles and seen videos lists"""
    if not is_authorised(update):
        await update.message.reply_text("⛔ Unauthorised!")
        return

    from shared.memory import clear_seen_articles, clear_seen_videos
    clear_seen_articles()
    clear_seen_videos()

    await update.message.reply_text(
        "🗑️ Seen content lists cleared!\n"
        "Next /check will return all available content fresh!"
    )


# Bot setup

def run_bot() -> None:
    """
    Build and start the Telegram bot with polling.
    """
    print("🤖 Content Monitor Telegram bot starting...")
    print(f"   Token loaded: {'✅' if BOT_TOKEN else '❌'}")
    print(f"   Chat ID loaded: {'✅' if CHAT_ID else '❌'}")

    # Build the application
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("check", check))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("clear", clear))

    print("✅ Bot ready! Send /start on Telegram to begin!")
    print("   Press Ctrl+C to stop\n")

    # Start polling — runs forever!
    app.run_polling()


if __name__ == "__main__":
    run_bot()
