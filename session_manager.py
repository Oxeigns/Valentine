import asyncio
import time
import uuid
from collections import defaultdict

SESSION_TIMEOUT = 300  # 5 minutes
MODE_COOLDOWN = 20
MAX_GROUP_SESSIONS = 10
MAX_USER_ACTIVE_SESSIONS = 3


class SessionManager:
    def __init__(self):
        self.sessions = defaultdict(dict)
        self.cooldowns = defaultdict(dict)
        self._cleanup_running = False

    async def start(self):
        """Start background cleanup task."""
        if not self._cleanup_running:
            self._cleanup_running = True
            asyncio.create_task(self._cleanup_task())

    async def _cleanup_task(self):
        while True:
            now = time.time()
            for group_id in list(self.sessions.keys()):
                for session_id in list(self.sessions[group_id].keys()):
                    session = self.sessions[group_id][session_id]
                    if now - session["created_at"] > SESSION_TIMEOUT:
                        del self.sessions[group_id][session_id]
                if not self.sessions[group_id]:
                    del self.sessions[group_id]
            await asyncio.sleep(30)

    async def create_session(self, group_id, mode, proposer_id, target_id):
        if len(self.sessions[group_id]) >= MAX_GROUP_SESSIONS:
            raise ValueError("Too many active love stories in this group. Try again in a moment.")

        active_by_proposer = sum(
            1 for session in self.sessions[group_id].values() if session["proposer_id"] == proposer_id
        )
        if active_by_proposer >= MAX_USER_ACTIVE_SESSIONS:
            raise ValueError("You already have too many active stories. Finish one first.")

        now = time.time()
        cooldown_key = (proposer_id, mode)
        last_used = self.cooldowns[group_id].get(cooldown_key)
        if last_used and now - last_used < MODE_COOLDOWN:
            wait_left = int(MODE_COOLDOWN - (now - last_used))
            raise ValueError(f"Cooldown active. Please wait {wait_left}s before using /{mode} again.")

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
            "status": "active",
        }
        self.sessions[group_id][session_id] = session
        self.cooldowns[group_id][cooldown_key] = now
        return session

    def get_session(self, group_id, session_id):
        return self.sessions.get(group_id, {}).get(session_id)

    def is_expired(self, session):
        return (time.time() - session["created_at"]) > SESSION_TIMEOUT

    def validate_participant(self, session, user_id):
        return user_id in {session["proposer_id"], session["target_id"]}

    def update_stage(self, group_id, session_id, stage):
        session = self.get_session(group_id, session_id)
        if session:
            session["stage"] = stage

    def increment_rejection(self, group_id, session_id):
        session = self.get_session(group_id, session_id)
        if session:
            session["rejection_count"] += 1

    async def end_session(self, group_id, session_id):
        if group_id in self.sessions:
            self.sessions[group_id].pop(session_id, None)
            if not self.sessions[group_id]:
                del self.sessions[group_id]

    async def delete_session(self, group_id, session_id):
        await self.end_session(group_id, session_id)
