# sar_system/telegram_bot.py
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
from sar_system.main import run_pipeline

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
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
        "Hey there👋! Still looking for some jobs?"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for /help command"""
    if not is_authorised(update):
        await update.message.reply_text("⛔ Unauthorised!")
        return

    await update.message.reply_text(
        "🤖 SAR Bot commands:\n\n"
        "/search — run full job search pipeline\n"
        "/status — show last report summary\n"
        "/clear  — reset seen jobs list\n"
        "/help   — show this message"
    )


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for /search command — triggers full SAR pipeline"""
    if not is_authorised(update):
        await update.message.reply_text("⛔ Unauthorised!")
        return

    await update.message.reply_text("🚀 SAR pipeline starting — this may take a minute...")

    try:
        # Run the pipeline — returns path to report file
        report_path = run_pipeline()

        if report_path is None:
            await update.message.reply_text(
                "⚠️ Pipeline completed but no relevant jobs found today!"
            )
            return

        # Read the report file
        with open(report_path, "r", encoding="utf-8") as f:
            report_content = f.read()

        # Split report into chunks if needed (4096 character limit per message)
        if len(report_content) <= 4096:
            await update.message.reply_text(report_content)
        else:
            chunks = [
                report_content[i:i+4096]
                for i in range(0, len(report_content), 4096)
            ]
            for chunk in chunks:
                await update.message.reply_text(chunk)

    except Exception as e:
        await update.message.reply_text(f"❌ Pipeline failed: {str(e)}")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for /status — shows most recent report summary"""
    if not is_authorised(update):
        await update.message.reply_text("⛔ Unauthorised!")
        return

    from sar_system.config import REPORTS_DIR

    # Find the most recent report file
    reports = sorted(REPORTS_DIR.glob("report_*.md"), reverse=True)

    if not reports:
        await update.message.reply_text("📭 No reports found yet — run /search first!")
        return

    latest_report = reports[0]
    date_str = latest_report.stem.replace("report_", "").replace("_", "-")

    await update.message.reply_text(
        f"📊 Latest report: {date_str}\n"
        f"📁 File: {latest_report.name}\n\n"
        f"Run /search to generate a fresh report!"
    )


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for /clear — resets seen jobs list"""
    if not is_authorised(update):
        await update.message.reply_text("⛔ Unauthorised!")
        return

    from shared.memory import clear_seen_jobs
    clear_seen_jobs()

    await update.message.reply_text(
        "🗑️ Seen jobs list cleared!\n"
        "Next /search will return all available jobs fresh!"
    )


# Bot setup

def run_bot() -> None:
    """
    Build and start the Telegram bot with polling.
    """
    print("🤖 SAR Telegram bot starting...")
    print(f"   Token loaded: {'✅' if BOT_TOKEN else '❌'}")
    print(f"   Chat ID loaded: {'✅' if CHAT_ID else '❌'}")

    # Build the application
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("search", search))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("clear", clear))

    print("✅ Bot ready! Send /start on Telegram to begin!")
    print("   Press Ctrl+C to stop\n")

    # Start polling — runs forever!
    app.run_polling()


if __name__ == "__main__":
    run_bot()