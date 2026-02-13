import os
from dataclasses import dataclass


@dataclass
class Config:
    API_ID: int
    API_HASH: str
    BOT_TOKEN: str

    @classmethod
    def load(cls):
        return cls(
            API_ID=int(os.getenv("API_ID")),
            API_HASH=os.getenv("API_HASH"),
            BOT_TOKEN=os.getenv("BOT_TOKEN"),
        )
