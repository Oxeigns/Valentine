import asyncio
import time
import uuid
import logging
from typing import Dict, Optional, Any

logger = logging.getLogger(__name__)


class SessionManager:
    """
    Handles:
    - Multi-session per group
    - Expiry
    - Cooldowns
    - Anti-spam
    """

    SESSION_TIMEOUT = 300  # 5 minutes
    COOLDOWN_SECONDS = 20
    MAX_GROUP_SESSIONS = 10
    MAX_USER_ACTIVE = 3

    def __init__(self):
        # sessions[group_id][session_id] = session_dict
        self.sessions: Dict[int, Dict[str, dict]] = {}

        # cooldowns[(user_id, mode)] = timestamp
        self.cooldowns: Dict[tuple, float] = {}

        # active sessions per user
        self.user_active_count: Dict[int, int] = {}

        # background cleanup
        asyncio.create_task(self._cleanup_task())

    # --------------------------------------------------
    # SESSION CREATION
    # --------------------------------------------------

    async def create_session(
        self,
        group_id: int,
        mode: str,
        proposer_id: int,
        target_id: Optional[int] = None
    ) -> dict:

        now = time.time()

        # Cooldown check
        if not self._check_cooldown(proposer_id, mode):
            raise Exception("⏳ You're moving too fast. Slow down.")

        # Max sessions per group
        if group_id in self.sessions:
            if len(self.sessions[group_id]) >= self.MAX_GROUP_SESSIONS:
                raise Exception("🚫 Too many love stories at once in this group.")

        # Max active per user
        if self.user_active_count.get(proposer_id, 0) >= self.MAX_USER_ACTIVE:
            raise Exception("🚫 You already have too many ongoing stories.")

        session_id = str(uuid.uuid4())[:8]

        session = {
            "session_id": session_id,
            "group_id": group_id,
            "mode": mode,
            "proposer_id": proposer_id,
            "target_id": target_id,
            "rejection_count": 0,
            "stage": "init",
            "created_at": now,
            "status": "active"
        }

        if group_id not in self.sessions:
            self.sessions[group_id] = {}

        self.sessions[group_id][session_id] = session
        self.user_active_count[proposer_id] = self.user_active_count.get(proposer_id, 0) + 1

        # apply cooldown
        self.cooldowns[(proposer_id, mode)] = now

        return session

    # --------------------------------------------------
    # GET SESSION
    # --------------------------------------------------

    def get_session(self, group_id: int, session_id: str) -> Optional[dict]:
        return self.sessions.get(group_id, {}).get(session_id)

    # --------------------------------------------------
    # UPDATE SESSION
    # --------------------------------------------------

    def update_stage(self, group_id: int, session_id: str, stage: str):
        session = self.get_session(group_id, session_id)
        if session:
            session["stage"] = stage

    def increment_rejection(self, group_id: int, session_id: str):
        session = self.get_session(group_id, session_id)
        if session:
            session["rejection_count"] += 1

    # --------------------------------------------------
    # END SESSION
    # --------------------------------------------------

    async def end_session(self, group_id: int, session_id: str):
        session = self.get_session(group_id, session_id)
        if not session:
            return

        proposer_id = session["proposer_id"]

        if proposer_id in self.user_active_count:
            self.user_active_count[proposer_id] -= 1
            if self.user_active_count[proposer_id] <= 0:
                del self.user_active_count[proposer_id]

        del self.sessions[group_id][session_id]

        if not self.sessions[group_id]:
            del self.sessions[group_id]

    # --------------------------------------------------
    # VALIDATION
    # --------------------------------------------------

    def validate_participant(self, session: dict, user_id: int) -> bool:
        return user_id in (session["proposer_id"], session["target_id"])

    def is_expired(self, session: dict) -> bool:
        return time.time() - session["created_at"] > self.SESSION_TIMEOUT

    # --------------------------------------------------
    # COOLDOWN
    # --------------------------------------------------

    def _check_cooldown(self, user_id: int, mode: str) -> bool:
        last = self.cooldowns.get((user_id, mode))
        if not last:
            return True
        return time.time() - last > self.COOLDOWN_SECONDS

    # --------------------------------------------------
    # CLEANUP TASK
    # --------------------------------------------------

    async def _cleanup_task(self):
        while True:
            await asyncio.sleep(30)
            for group_id in list(self.sessions.keys()):
                for session_id in list(self.sessions[group_id].keys()):
                    session = self.sessions[group_id][session_id]
                    if self.is_expired(session):
                        logger.info(f"Session expired: {session_id}")
                        await self.end_session(group_id, session_id)
