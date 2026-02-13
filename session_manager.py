import asyncio
import time
import uuid
from collections import defaultdict

SESSION_TIMEOUT = 300  # 5 minutes


class SessionManager:
    def __init__(self):
        self.sessions = defaultdict(dict)
        self.cooldowns = defaultdict(dict)
        self._cleanup_running = False

    async def start(self):
        """
        Start background cleanup task.
        Must be called AFTER event loop starts.
        """
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

    def create_session(self, group_id, mode, proposer_id, target_id):
        if len(self.sessions[group_id]) >= 10:
            return None

        session_id = str(uuid.uuid4())[:8]

        self.sessions[group_id][session_id] = {
            "session_id": session_id,
            "group_id": group_id,
            "mode": mode,
            "proposer_id": proposer_id,
            "target_id": target_id,
            "rejection_count": 0,
            "stage": "init",
            "created_at": time.time(),
            "status": "active",
        }

        return session_id

    def get_session(self, group_id, session_id):
        return self.sessions.get(group_id, {}).get(session_id)

    def delete_session(self, group_id, session_id):
        if group_id in self.sessions:
            self.sessions[group_id].pop(session_id, None)
