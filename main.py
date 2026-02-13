import logging
from typing import Optional

from pyrogram import Client, filters, idle
from pyrogram.types import CallbackQuery, Message

from breakup_engine import BreakupEngine
from config import Config
from crush_engine import CrushEngine
from keyboards import main_menu
from leaderboard import Leaderboard
from prank_engine import PrankEngine
from proposal_engine import ProposalEngine
from session_manager import SessionManager


# --------------------------------------------------
# LOGGING
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# INITIALIZE CONFIG
# --------------------------------------------------

config = Config.load()


# --------------------------------------------------
# INITIALIZE BOT CLIENT
# --------------------------------------------------

app = Client(
    name="love-game-bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    in_memory=True,
    workers=50,
)


# --------------------------------------------------
# CORE SYSTEMS
# --------------------------------------------------

session_manager = SessionManager()
leaderboard = Leaderboard()

proposal_engine = ProposalEngine(app, session_manager, leaderboard)
crush_engine = CrushEngine(app, session_manager, leaderboard)
prank_engine = PrankEngine(app, session_manager, leaderboard)
breakup_engine = BreakupEngine(app, session_manager)


# --------------------------------------------------
# COMMAND ROUTING
# --------------------------------------------------

SUPPORTED_COMMANDS = [
    "love",
    "propose",
    "crush",
    "prank",
    "breakup",
    "loveboard",
    "help",
]

BOT_USERNAME: Optional[str] = None


async def _resolve_command(message: Message) -> Optional[str]:
    if not message.text:
        return None

    token = message.text.split(maxsplit=1)[0].strip()
    if not token.startswith("/"):
        return None

    core = token[1:]
    command = core
    mention = None

    if "@" in core:
        command, mention = core.split("@", 1)

    command = command.lower()
    if command not in SUPPORTED_COMMANDS:
        return None

    global BOT_USERNAME
    if mention:
        if BOT_USERNAME is None:
            me = await app.get_me()
            BOT_USERNAME = (me.username or "").lower()
        if mention.lower() != BOT_USERNAME:
            return None

    return command


@app.on_message(filters.command(SUPPORTED_COMMANDS, prefixes=["/"]))
async def command_router(client: Client, message: Message):
    try:
        command = await _resolve_command(message)
        if not command:
            return

        if message.chat.type not in {"group", "supergroup"}:
            await message.reply("This bot works in groups and supergroups only 💞")
            return

        logger.info(
            "Command received: /%s | chat_id=%s | user_id=%s | raw=%s",
            command,
            message.chat.id,
            message.from_user.id if message.from_user else "unknown",
            message.text,
        )

        if command == "love":
            await message.reply(
                "💖 **Welcome to the Love Game Engine**\n\n"
                "Choose your destiny below.",
                reply_markup=main_menu(),
            )
            return

        if command == "propose":
            await proposal_engine.start(message)
            return

        if command == "crush":
            await crush_engine.start(message)
            return

        if command == "prank":
            await prank_engine.start(message)
            return

        if command == "breakup":
            await breakup_engine.start(message)
            return

        if command == "loveboard":
            text = await leaderboard.format_leaderboard(message.chat.id)
            await message.reply(text)
            return

        if command == "help":
            await message.reply(
                "📖 **Love Game Help**\n\n"
                "/love – Open menu\n"
                "/propose – Real proposal (reply required)\n"
                "/crush – Anonymous crush (reply required)\n"
                "/prank – Fake proposal prank (reply required)\n"
                "/breakup – End your love story\n"
                "/loveboard – View rankings\n\n"
                "Each love story runs separately.\n"
                "Sessions expire after 5 minutes.\n"
                "Cooldown: 20 seconds per mode."
            )

    except Exception as exc:
        logger.exception("Command handler error: %s", exc)


# --------------------------------------------------
# CALLBACK ROUTER
# --------------------------------------------------


@app.on_callback_query()
async def callback_router(client: Client, callback: CallbackQuery):
    try:
        if not callback.data:
            return

        if callback.data.startswith("menu|"):
            action = callback.data.split("|", 1)[1]

            if action == "leaderboard":
                text = await leaderboard.format_leaderboard(callback.message.chat.id)
                await callback.message.edit_text(text)
                return

            if action == "help":
                await callback.message.edit_text(
                    "📖 **Love Game Help**\n\n"
                    "Reply to someone before starting a mode.\n"
                    "Each love story runs separately.\n"
                    "Sessions expire after 5 minutes.\n"
                    "Cooldown: 20 seconds per mode."
                )
                return

            await callback.answer()
            return

        if callback.data.startswith("love|proposal"):
            await proposal_engine.handle_callback(callback)
        elif callback.data.startswith("love|crush"):
            await crush_engine.handle_callback(callback)
        elif callback.data.startswith("love|prank"):
            await prank_engine.handle_callback(callback)
        elif callback.data.startswith("love|breakup"):
            await breakup_engine.handle_callback(callback)
        else:
            await callback.answer("Unknown action.")

    except Exception as exc:
        logger.exception("Callback error: %s", exc)
        await callback.answer("Something went wrong.")


# --------------------------------------------------
# MAIN ENTRY
# --------------------------------------------------


async def main():
    logger.info("Starting Love Game Engine...")
    await app.start()
    await session_manager.start()

    try:
        global BOT_USERNAME
        me = await app.get_me()
        BOT_USERNAME = (me.username or "").lower()

        logger.info("Love Game Engine is LIVE ❤️")
        await idle()
    finally:
        await app.stop()


# --------------------------------------------------
# RUN
# --------------------------------------------------

if __name__ == "__main__":
    app.run(main())
