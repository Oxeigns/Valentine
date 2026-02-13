import logging
from pyrogram import Client
from pyrogram.types import Message, CallbackQuery
from session_manager import SessionManager
from leaderboard import Leaderboard
from storage import JSONStorage
from keyboards import proposal_start, proposal_response
from utils import (
    mention,
    parse_callback,
    proposal_build_up,
    proposal_success,
    proposal_rejection,
    cinematic_delay,
    not_yours_message,
    expired_message
)

logger = logging.getLogger(__name__)


class ProposalEngine:

    def __init__(
        self,
        app: Client,
        session_manager: SessionManager,
        leaderboard: Leaderboard
    ):
        self.app = app
        self.sessions = session_manager
        self.leaderboard = leaderboard
        self.couples_storage = JSONStorage("couples.json")

    # --------------------------------------------------
    # START PROPOSAL
    # --------------------------------------------------

    async def start(self, message: Message):

        if not message.reply_to_message:
            await message.reply("Reply to someone to propose 💘")
            return

        group_id = message.chat.id
        proposer = message.from_user
        target = message.reply_to_message.from_user

        try:
            session = await self.sessions.create_session(
                group_id=group_id,
                mode="proposal",
                proposer_id=proposer.id,
                target_id=target.id
            )
        except Exception as e:
            await message.reply(str(e))
            return

        build_up = proposal_build_up(target.first_name)

        await message.reply(
            f"{build_up}\n\n"
            f"{mention(proposer.id, proposer.first_name)} "
            f"is about to confess something…",
            reply_markup=proposal_start(session["session_id"]),
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

        # Only participants allowed
        if not self.sessions.validate_participant(session, user_id):
            await callback.answer(not_yours_message(), show_alert=True)
            return

        # --------------------------------------------------
        # CONFESS STAGE
        # --------------------------------------------------

        if action == "confess" and user_id == session["proposer_id"]:
            self.sessions.update_stage(group_id, session_id, "confessed")

            await callback.message.edit_text(
                f"{mention(session['target_id'], 'You')}...\n\n"
                "Someone has feelings for you. ❤️",
                reply_markup=proposal_response(session_id),
                disable_web_page_preview=True
            )
            await callback.answer()

        # --------------------------------------------------
        # ACCEPT
        # --------------------------------------------------

        elif action == "accept" and user_id == session["target_id"]:

            proposer = await self.app.get_users(session["proposer_id"])
            target = await self.app.get_users(session["target_id"])

            success_text = proposal_success(
                mention(proposer.id, proposer.first_name),
                mention(target.id, target.first_name)
            )

            await callback.message.edit_text(success_text)

            # Save couple
            couples = await self.couples_storage.get(str(group_id), {})
            couples[str(proposer.id)] = target.id
            await self.couples_storage.set(str(group_id), couples)

            # Update leaderboard
            await self.leaderboard.add_proposal(group_id, proposer.id)

            await self.sessions.end_session(group_id, session_id)
            await callback.answer("Love accepted 💞")

        # --------------------------------------------------
        # REJECT
        # --------------------------------------------------

        elif action == "reject" and user_id == session["target_id"]:

            self.sessions.increment_rejection(group_id, session_id)

            await self.leaderboard.add_rejection(group_id, session["proposer_id"])

            if session["rejection_count"] >= 5:
                await callback.message.edit_text(
                    "💔 Final rejection.\n\n"
                    "The love story ends here."
                )
                await self.sessions.end_session(group_id, session_id)
                await callback.answer("Love story ended.")
                return

            await callback.answer("Ouch 💔")

            await callback.message.edit_text(
                proposal_rejection(),
                reply_markup=proposal_response(session_id)
            )

        # --------------------------------------------------
        # THINKING
        # --------------------------------------------------

        elif action == "thinking" and user_id == session["target_id"]:
            await callback.answer("Thinking...")
            await cinematic_delay(2)
            await callback.answer("Still thinking... 🤔")

        # --------------------------------------------------
        # HINT
        # --------------------------------------------------

        elif action == "hint" and user_id == session["target_id"]:

            proposer = await self.app.get_users(session["proposer_id"])

            await callback.answer(
                f"Hint: Their name starts with '{proposer.first_name[0]}' 😉",
                show_alert=True
            )
        else:
            await callback.answer("Yeh button ab valid nahi hai.", show_alert=True)
