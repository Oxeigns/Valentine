import logging
from pyrogram import Client
from pyrogram.types import Message, CallbackQuery
from session_manager import SessionManager
from leaderboard import Leaderboard
from keyboards import crush_target, crush_reveal_decision
from utils import (
    mention,
    parse_callback,
    crush_message,
    crush_secret_kept,
    not_yours_message,
    expired_message
)

logger = logging.getLogger(__name__)


class CrushEngine:

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
    # START CRUSH
    # --------------------------------------------------

    async def start(self, message: Message):

        if not message.reply_to_message:
            await message.reply("Reply to your crush 😏")
            return

        group_id = message.chat.id
        proposer = message.from_user
        target = message.reply_to_message.from_user

        try:
            session = await self.sessions.create_session(
                group_id=group_id,
                mode="crush",
                proposer_id=proposer.id,
                target_id=target.id
            )
        except Exception as e:
            await message.reply(str(e))
            return

        await self.leaderboard.add_crush(group_id, proposer.id)

        await message.reply(
            crush_message(),
            reply_markup=crush_target(session["session_id"])
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

        # --------------------------------------------------
        # TARGET PRESSES REVEAL
        # --------------------------------------------------

        if action == "reveal" and user_id == session["target_id"]:

            await callback.answer()

            await callback.message.edit_text(
                "The admirer must decide...\n\n"
                "Should the identity be revealed?",
                reply_markup=crush_reveal_decision(session_id)
            )

        # --------------------------------------------------
        # TARGET IGNORES
        # --------------------------------------------------

        elif action == "ignore" and user_id == session["target_id"]:

            await callback.answer("Secret ignored 🙈")
            await callback.message.delete()
            await self.sessions.end_session(group_id, session_id)

        # --------------------------------------------------
        # PROPOSER CHOOSES TO REVEAL
        # --------------------------------------------------

        elif action == "yes_reveal" and user_id == session["proposer_id"]:

            proposer = await self.app.get_users(session["proposer_id"])
            target = await self.app.get_users(session["target_id"])

            await callback.message.edit_text(
                f"💌 Mystery solved.\n\n"
                f"It was {mention(proposer.id, proposer.first_name)} "
                f"who had a crush on "
                f"{mention(target.id, target.first_name)} ❤️",
                disable_web_page_preview=True
            )

            await self.sessions.end_session(group_id, session_id)
            await callback.answer("Identity revealed 💫")

        # --------------------------------------------------
        # PROPOSER KEEPS SECRET
        # --------------------------------------------------

        elif action == "no_reveal" and user_id == session["proposer_id"]:

            await callback.message.edit_text(crush_secret_kept())
            await self.sessions.end_session(group_id, session_id)
            await callback.answer("Secret kept 🔒")
        else:
            await callback.answer("Yeh action ab allow nahi hai.", show_alert=True)
