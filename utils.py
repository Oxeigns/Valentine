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
        "The air feels different tonight… 🌙",
        "Some feelings can’t stay hidden anymore…",
        "Destiny has chosen this moment…",
        f"{name}, this message carries a heartbeat… ❤️",
        "Silence before the confession…",
        "Violins are playing in the background (probably). 🎻",
        "Chat slow ho gaya… kyunki confession loading hai. 💘",
        "Aaj group me sirf emotions chalenge, logic nahi. ✨"
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
        "The drama intensifies…",
        "Dil tut gaya, lekin attitude abhi bhi premium hai.",
        "Plot twist: hero arc starts after heartbreak."
    ]
    return random.choice(lines)


def crush_message() -> str:
    lines = [
        (
            "💌 Someone in this group has a crush on you…\n\n"
            "They’ve been watching silently.\n"
            "Admiring quietly.\n"
            "Waiting patiently.\n\n"
            "Will you reveal the mystery?"
        ),
        (
            "🌹 Anonymous heartbeat detected.\n\n"
            "Kisi ne aapke liye feelings drop ki hain.\n"
            "Naam abhi secret hai.\n\n"
            "Ready for reveal?"
        ),
        (
            "✨ Love radar says: you are someone’s favorite person in this group.\n\n"
            "Identity hidden. Emotions real."
        )
    ]
    return random.choice(lines)


def crush_secret_kept() -> str:
    lines = [
        "🔒 Some secrets are more beautiful when hidden.",
        "🔒 Mystery maintained. Dil ka password safe hai.",
        "🌙 Secret crush archived in moonlight mode."
    ]
    return random.choice(lines)


def prank_dramatic(name: str) -> str:
    lines = [
        (
            f"💘 {name}…\n\n"
            "This is not a normal message.\n"
            "This is not a joke.\n"
            "This is destiny speaking."
        ),
        (
            f"🎭 {name}, scene set hai.\n\n"
            "Lights on. Heartbeat up.\n"
            "Aur ab… plot twist incoming."
        )
    ]
    return random.choice(lines)


def prank_reveal(proposer: str) -> str:
    lines = [
        (
            f"Relax… it was a prank 😏\n\n"
            f"Blame {proposer}.\n"
            "Trust issues unlocked."
        ),
        (
            f"😂 Scene complete. Yeh prank tha.\n\n"
            f"Mastermind: {proposer}.\n"
            "Audience reaction: legendary."
        )
    ]
    return random.choice(lines)


def breakup_archived() -> str:
    lines = [
        (
            "💔 Love story archived.\n\n"
            "The memories remain.\n"
            "The couple is no more."
        ),
        (
            "🖤 Chapter closed.\n\n"
            "Photos fade. Status changes.\n"
            "A new era begins."
        )
    ]
    return random.choice(lines)


def welcome_text() -> str:
    lines = [
        "💖 **Welcome to Valentine Premium Mode**\n\nDrama on. Hearts open. Choose your destiny below.",
        "🌹 **Welcome to the Love Arena**\n\nPropose, prank, confess, breakup — everything cinematic.",
        "✨ **Valentine Engine Activated**\n\nAaj group me sirf premium vibes. Pick a mode below."
    ]
    return random.choice(lines)


def help_text() -> str:
    return (
        "📖 **Love Game Help (Premium)**\n\n"
        "/love – Open cinematic menu\n"
        "/propose – Real proposal (reply required)\n"
        "/crush – Anonymous crush (reply required)\n"
        "/prank – Fake proposal prank (reply required)\n"
        "/breakup – End your love story\n"
        "/loveboard – View rankings\n"
        "/vibe – Drop a fresh Valentine vibe\n\n"
        "Each love story runs separately.\n"
        "Sessions expire after 5 minutes.\n"
        "Cooldown: 20 seconds per mode."
    )


def random_vibe() -> str:
    vibes = [
        "💘 Vibe: Aaj proposal ka perfect day hai. Risk lo, history banao.",
        "🌙 Vibe: Late-night confession energy unlocked.",
        "🎭 Vibe: Thoda pyaar, thoda prank — perfect combo.",
        "💔 Vibe: Breakup bhi classy hona chahiye, drama ke saath.",
        "✨ Vibe: Group chat ko movie scene bana do."
    ]
    return random.choice(vibes)


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
