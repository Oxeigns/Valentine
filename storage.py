import json
import asyncio
import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class JSONStorage:
    """
    Async-safe JSON persistent storage.
    Used for:
    - Couples
    - Leaderboard
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self._lock = asyncio.Lock()
        self._data: Dict[str, Any] = {}
        self._ensure_file()
        self._load()

    # --------------------------------------------------
    # INITIALIZATION
    # --------------------------------------------------

    def _ensure_file(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump({}, f)

    def _load(self):
        try:
            with open(self.file_path, "r") as f:
                self._data = json.load(f)
        except Exception as e:
            logger.error(f"Storage load failed: {e}")
            self._data = {}

    async def _save(self):
        async with self._lock:
            temp_file = self.file_path + ".tmp"
            try:
                with open(temp_file, "w") as f:
                    json.dump(self._data, f, indent=4)
                os.replace(temp_file, self.file_path)
            except Exception as e:
                logger.error(f"Storage save failed: {e}")

    # --------------------------------------------------
    # GENERIC METHODS
    # --------------------------------------------------

    async def get(self, key: str, default=None):
        return self._data.get(key, default)

    async def set(self, key: str, value: Any):
        self._data[key] = value
        await self._save()

    async def delete(self, key: str):
        if key in self._data:
            del self._data[key]
            await self._save()

    async def all(self):
        return self._data

    async def update_nested(self, main_key: str, sub_key: str, value: Any):
        if main_key not in self._data:
            self._data[main_key] = {}
        self._data[main_key][sub_key] = value
        await self._save()

    async def increment_nested(self, main_key: str, sub_key: str, amount: int = 1):
        if main_key not in self._data:
            self._data[main_key] = {}
        self._data[main_key][sub_key] = self._data[main_key].get(sub_key, 0) + amount
        await self._save()
