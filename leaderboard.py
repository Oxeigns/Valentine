import logging
from typing import Dict, List, Tuple
from storage import JSONStorage

logger = logging.getLogger(__name__)


class Leaderboard:
    """
    Tracks love statistics per group.
    Persistent via JSON.
    """

    def __init__(self):
        self.storage = JSONStorage("leaderboard.json")

    # --------------------------------------------------
    # INTERNAL STRUCTURE
    # leaderboard.json format:
    #
    # {
    #   "group_id": {
    #       "user_id": {
    #           "proposals": 0,
    #           "rejections": 0,
    #           "pranks": 0,
    #           "crushes": 0
    #       }
    #   }
    # }
    # --------------------------------------------------

    async def _ensure_user(self, group_id: int, user_id: int):
        group_data = await self.storage.get(str(group_id), {})
        if str(user_id) not in group_data:
            group_data[str(user_id)] = {
                "proposals": 0,
                "rejections": 0,
                "pranks": 0,
                "crushes": 0
            }
            await self.storage.set(str(group_id), group_data)

    # --------------------------------------------------
    # STAT UPDATERS
    # --------------------------------------------------

    async def add_proposal(self, group_id: int, user_id: int):
        await self._ensure_user(group_id, user_id)
        group_data = await self.storage.get(str(group_id))
        group_data[str(user_id)]["proposals"] += 1
        await self.storage.set(str(group_id), group_data)

    async def add_rejection(self, group_id: int, user_id: int):
        await self._ensure_user(group_id, user_id)
        group_data = await self.storage.get(str(group_id))
        group_data[str(user_id)]["rejections"] += 1
        await self.storage.set(str(group_id), group_data)

    async def add_prank(self, group_id: int, user_id: int):
        await self._ensure_user(group_id, user_id)
        group_data = await self.storage.get(str(group_id))
        group_data[str(user_id)]["pranks"] += 1
        await self.storage.set(str(group_id), group_data)

    async def add_crush(self, group_id: int, user_id: int):
        await self._ensure_user(group_id, user_id)
        group_data = await self.storage.get(str(group_id))
        group_data[str(user_id)]["crushes"] += 1
        await self.storage.set(str(group_id), group_data)

    # --------------------------------------------------
    # RANKING LOGIC
    # --------------------------------------------------

    async def get_group_ranking(self, group_id: int) -> List[Tuple[str, dict]]:
        group_data: Dict[str, dict] = await self.storage.get(str(group_id), {})
        sorted_users = sorted(
            group_data.items(),
            key=lambda x: x[1]["proposals"],
            reverse=True
        )
        return sorted_users

    async def format_leaderboard(self, group_id: int) -> str:
        ranking = await self.get_group_ranking(group_id)

        if not ranking:
            return "🏆 No love stories yet in this group..."

        text = "🏆 **Loveboard Rankings**\n\n"

        medals = ["🥇", "🥈", "🥉"]

        for index, (user_id, stats) in enumerate(ranking[:10]):
            medal = medals[index] if index < 3 else "💎"

            title = self._get_title(index)

            text += (
                f"{medal} {title}\n"
                f"👤 User: `{user_id}`\n"
                f"💘 Proposals: {stats['proposals']}\n"
                f"💔 Rejections: {stats['rejections']}\n"
                f"🎭 Pranks: {stats['pranks']}\n"
                f"💌 Crushes: {stats['crushes']}\n\n"
            )

        return text

    # --------------------------------------------------
    # TITLE SYSTEM
    # --------------------------------------------------

    def _get_title(self, position: int) -> str:
        if position == 0:
            return "Group Romeo"
        elif position == 1:
            return "Heart Collector"
        elif position == 2:
            return "Drama King/Queen"
        else:
            return "Love Challenger"
