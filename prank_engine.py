import logging
from pyrogram import Client
from pyrogram.types import Message, CallbackQuery
from session_manager import SessionManager
from leaderboard import Leaderboard
from keyboards import prank_final
from utils import (
    mention,
    parse_callback,
    prank_dramatic,
    prank_reveal,
    not_yours_message,
    expired_message
)

logger = logging.getLogger(__name__)


class PrankEngine:

    def __init__(
        self,
        app: Client,
        session_manager: SessionManager,
        leaderboard: Leaderboard
    ):
        self.app = app
        self.sessions = session_manager
        self.leaderboard = leaderboard

    # --------------------------------------------------
    # START PRANK
    # --------------------------------------------------

    async def start(self, message: Message):

        if not message.reply_to_message:
            await message.reply("Reply target select karo aur /prank se scene shuru karo 😈")
            return

        group_id = message.chat.id
        proposer = message.from_user
        target = message.reply_to_message.from_user

        try:
            session = await self.sessions.create_session(
                group_id=group_id,
                mode="prank",
                proposer_id=proposer.id,
                target_id=target.id
            )
        except Exception as e:
            await message.reply(str(e))
            return

        # Update leaderboard prank stat
        await self.leaderboard.add_prank(group_id, proposer.id)

        dramatic_text = prank_dramatic(target.first_name)

        await message.reply(
            dramatic_text,
            reply_markup=prank_final(session["session_id"])
        )

    # --------------------------------------------------
    # HANDLE CALLBACK
    # --------------------------------------------------

    async def handle_callback(self, callback: CallbackQuery):

        prefix, mode, session_id, action = parse_callback(callback.data)
        group_id = callback.message.chat.id

        session = self.sessions.get_session(group_id, session_id)

        if not session:
            await callback.answer(expired_message(), show_alert=True)
            return

        if self.sessions.is_expired(session):
            await self.sessions.end_session(group_id, session_id)
            await callback.answer(expired_message(), show_alert=True)
            return

        user_id = callback.from_user.id

        # Only participants allowed
        if not self.sessions.validate_participant(session, user_id):
            await callback.answer(not_yours_message(), show_alert=True)
            return

        proposer = await self.app.get_users(session["proposer_id"])

        # --------------------------------------------------
        # TARGET PRESSES ACCEPT
        # --------------------------------------------------

        if action == "accept" and user_id == session["target_id"]:

            await callback.message.edit_text(
                prank_reveal(mention(proposer.id, proposer.first_name)),
                disable_web_page_preview=True
            )

            await self.sessions.end_session(group_id, session_id)
            await callback.answer("Gotcha. Oscar-level acting 😏")

        # --------------------------------------------------
        # TARGET PRESSES 'IT'S A PRANK'
        # --------------------------------------------------

        elif action == "prank_reveal" and user_id == session["target_id"]:

            await callback.message.edit_text(
                "😂 You can’t prank the prank master.\n\nRespect earned. Aura +100.",
            )

            await self.sessions.end_session(group_id, session_id)
            await callback.answer("Savage move. Crowd cheering 😎")
        else:
            await callback.answer("Yeh prank button ab kaam ka nahi raha.", show_alert=True)
