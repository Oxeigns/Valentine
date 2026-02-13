import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery

from config import Config
from session_manager import SessionManager
from leaderboard import Leaderboard
from keyboards import main_menu
from proposal_engine import ProposalEngine
from crush_engine import CrushEngine
from prank_engine import PrankEngine
from breakup_engine import BreakupEngine


# --------------------------------------------------
# LOGGING
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# INITIALIZE APP
# --------------------------------------------------

config = Config.load()

app = Client(
    "love-game-bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

session_manager = SessionManager()
leaderboard = Leaderboard()

proposal_engine = ProposalEngine(app, session_manager, leaderboard)
crush_engine = CrushEngine(app, session_manager, leaderboard)
prank_engine = PrankEngine(app, session_manager, leaderboard)
breakup_engine = BreakupEngine(app, session_manager)


# --------------------------------------------------
# COMMAND HANDLERS
# --------------------------------------------------

@app.on_message(filters.command("love") & filters.group)
async def love_menu(client: Client, message: Message):
    await message.reply(
        "💖 Welcome to the Love Game Engine\n\n"
        "Choose your destiny below.",
        reply_markup=main_menu()
    )


@app.on_message(filters.command("propose") & filters.group)
async def propose_cmd(client: Client, message: Message):
    await proposal_engine.start(message)


@app.on_message(filters.command("crush") & filters.group)
async def crush_cmd(client: Client, message: Message):
    await crush_engine.start(message)


@app.on_message(filters.command("prank") & filters.group)
async def prank_cmd(client: Client, message: Message):
    await prank_engine.start(message)


@app.on_message(filters.command("breakup") & filters.group)
async def breakup_cmd(client: Client, message: Message):
    await breakup_engine.start(message)


@app.on_message(filters.command("loveboard") & filters.group)
async def loveboard_cmd(client: Client, message: Message):
    text = await leaderboard.format_leaderboard(message.chat.id)
    await message.reply(text)


@app.on_message(filters.command("help") & filters.group)
async def help_cmd(client: Client, message: Message):
    await message.reply(
        "📖 Love Game Help\n\n"
        "/love – Open menu\n"
        "/propose – Real proposal (reply to user)\n"
        "/crush – Anonymous crush (reply to user)\n"
        "/prank – Fake proposal prank (reply to user)\n"
        "/breakup – End your love story\n"
        "/loveboard – View rankings\n\n"
        "Make sure you reply to someone when required."
    )


# --------------------------------------------------
# CALLBACK ROUTER
# --------------------------------------------------

@app.on_callback_query()
async def callback_router(client: Client, callback: CallbackQuery):

    if not callback.data:
        return

    if callback.data.startswith("menu|"):
        action = callback.data.split("|")[1]

        if action == "leaderboard":
            text = await leaderboard.format_leaderboard(callback.message.chat.id)
            await callback.message.edit_text(text)
            return

        if action == "help":
            await callback.message.edit_text(
                "📖 Love Game Help\n\n"
                "Reply to someone before starting a mode.\n"
                "Each love story runs separately.\n"
                "Sessions expire after 5 minutes.\n"
                "Cooldown: 20 seconds per mode."
            )
            return

        await callback.answer()
        return

    # Route by mode
    if callback.data.startswith("love|proposal"):
        await proposal_engine.handle_callback(callback)

    elif callback.data.startswith("love|crush"):
        await crush_engine.handle_callback(callback)

    elif callback.data.startswith("love|prank"):
        await prank_engine.handle_callback(callback)

    elif callback.data.startswith("love|breakup"):
        await breakup_engine.handle_callback(callback)


# --------------------------------------------------
# START BOT
# --------------------------------------------------

async def main():
    logger.info("Starting Love Game Engine...")
    await app.start()
    logger.info("Love Game Engine is live.")
    await idle()


from pyrogram import idle

if __name__ == "__main__":
    asyncio.run(main())
