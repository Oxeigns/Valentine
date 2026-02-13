import asyncio
import random
from typing import Tuple


# --------------------------------------------------
# USER FORMATTER
# --------------------------------------------------

def mention(user_id: int, name: str) -> str:
    return f"[{name}](tg://user?id={user_id})"


# --------------------------------------------------
# CALLBACK PARSER
# love|mode|session_id|action
# --------------------------------------------------

def parse_callback(data: str) -> Tuple[str, str, str, str]:
    try:
        prefix, mode, session_id, action = data.split("|")
        return prefix, mode, session_id, action
    except Exception:
        return None, None, None, None


# --------------------------------------------------
# DRAMATIC TEXT GENERATORS
# --------------------------------------------------

def proposal_build_up(name: str) -> str:
    lines = [
        f"The air feels different tonight… 🌙",
        f"Some feelings can’t stay hidden anymore…",
        f"Destiny has chosen this moment…",
        f"{name}, this message carries a heartbeat… ❤️",
        f"Silence before the confession…"
    ]
    return random.choice(lines)


def proposal_success(proposer: str, target: str) -> str:
    return (
        f"💞 And just like that… a new love story begins.\n\n"
        f"{proposer} ❤️ {target}\n\n"
        f"The group witnesses history tonight."
    )


def proposal_rejection() -> str:
    lines = [
        "Love is brave… but sometimes not returned. 💔",
        "That hurt echoed across the group…",
        "Rejection builds character… allegedly.",
        "The drama intensifies…"
    ]
    return random.choice(lines)


def crush_message() -> str:
    return (
        "💌 Someone in this group has a crush on you…\n\n"
        "They’ve been watching silently.\n"
        "Admiring quietly.\n"
        "Waiting patiently.\n\n"
        "Will you reveal the mystery?"
    )


def crush_secret_kept() -> str:
    return "🔒 Some secrets are more beautiful when hidden."


def prank_dramatic(name: str) -> str:
    return (
        f"💘 {name}…\n\n"
        "This is not a normal message.\n"
        "This is not a joke.\n"
        "This is destiny speaking."
    )


def prank_reveal(proposer: str) -> str:
    return (
        f"Relax… it was a prank 😏\n\n"
        f"Blame {proposer}.\n"
        "Trust issues unlocked."
    )


def breakup_archived() -> str:
    return (
        "💔 Love story archived.\n\n"
        "The memories remain.\n"
        "The couple is no more."
    )


# --------------------------------------------------
# DELAY UTILITY (CINEMATIC PAUSE)
# --------------------------------------------------

async def cinematic_delay(seconds: float):
    await asyncio.sleep(seconds)


# --------------------------------------------------
# PERMISSION VALIDATION
# --------------------------------------------------

def not_yours_message() -> str:
    return "🚫 This love story isn’t yours."


def expired_message() -> str:
    return "⌛ This love story has faded away..."
