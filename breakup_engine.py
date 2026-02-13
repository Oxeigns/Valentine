import logging
from pyrogram import Client
from pyrogram.types import Message, CallbackQuery
from session_manager import SessionManager
from storage import JSONStorage
from keyboards import breakup_confirm
from utils import (
    mention,
    parse_callback,
    breakup_archived,
    cinematic_delay,
    not_yours_message,
    expired_message
)

logger = logging.getLogger(__name__)


class BreakupEngine:

    def __init__(
        self,
        app: Client,
        session_manager: SessionManager
    ):
        self.app = app
        self.sessions = session_manager
        self.couples_storage = JSONStorage("couples.json")

    # --------------------------------------------------
    # START BREAKUP
    # --------------------------------------------------

    async def start(self, message: Message):

        group_id = message.chat.id
        user = message.from_user

        couples = await self.couples_storage.get(str(group_id), {})

        partner_id = couples.get(str(user.id))

        if not partner_id:
            await message.reply("💔 Tum currently kisi registered love story me nahi ho.")
            return

        try:
            session = await self.sessions.create_session(
                group_id=group_id,
                mode="breakup",
                proposer_id=user.id,
                target_id=partner_id
            )
        except Exception as e:
            await message.reply(str(e))
            return

        partner = await self.app.get_users(partner_id)

        await message.reply(
            f"{mention(user.id, user.first_name)} wants to end the love story with "
            f"{mention(partner.id, partner.first_name)}…\n\n"
            "Kya yahi the end hai, ya last chance bacha hai?",
            reply_markup=breakup_confirm(session["session_id"]),
            disable_web_page_preview=True
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

        # Only couple members allowed
        if not self.sessions.validate_participant(session, user_id):
            await callback.answer(not_yours_message(), show_alert=True)
            return

        # --------------------------------------------------
        # CONFIRM BREAKUP
        # --------------------------------------------------

        if action == "confirm":

            await callback.answer("Processing heartbreak... 💔")

            await cinematic_delay(2)

            couples = await self.couples_storage.get(str(group_id), {})

            # Remove both directions
            proposer_id = session["proposer_id"]
            target_id = session["target_id"]

            couples.pop(str(proposer_id), None)
            couples.pop(str(target_id), None)

            await self.couples_storage.set(str(group_id), couples)

            await callback.message.edit_text(breakup_archived())

            await self.sessions.end_session(group_id, session_id)

        # --------------------------------------------------
        # CANCEL
        # --------------------------------------------------

        elif action == "cancel":

            await callback.answer("Breakup cancelled. Pyaar wins 🥺")
            await callback.message.edit_text("💞 Love story continues. Audience emotional ho gayi.")
            await self.sessions.end_session(group_id, session_id)
        else:
            await callback.answer("Yeh option valid nahi hai.", show_alert=True)
