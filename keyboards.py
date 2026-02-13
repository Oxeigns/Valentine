from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# --------------------------------------------------
# MAIN MENU
# --------------------------------------------------

def main_menu():
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("💘 Real Proposal", callback_data="menu|proposal")],
            [InlineKeyboardButton("💌 Anonymous Crush", callback_data="menu|crush")],
            [InlineKeyboardButton("🎭 Fake Proposal Prank", callback_data="menu|prank")],
            [InlineKeyboardButton("💔 Breakup", callback_data="menu|breakup")],
            [InlineKeyboardButton("🏆 Loveboard", callback_data="menu|leaderboard")],
            [InlineKeyboardButton("📖 Help", callback_data="menu|help")],
        ]
    )


# --------------------------------------------------
# REAL PROPOSAL BUTTONS
# --------------------------------------------------

def proposal_start(session_id: str):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "💌 Confess Feelings",
                    callback_data=f"love|proposal|{session_id}|confess"
                )
            ]
        ]
    )


def proposal_response(session_id: str):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "💖 Accept",
                    callback_data=f"love|proposal|{session_id}|accept"
                )
            ],
            [
                InlineKeyboardButton(
                    "🤔 Thinking...",
                    callback_data=f"love|proposal|{session_id}|thinking"
                )
            ],
            [
                InlineKeyboardButton(
                    "💔 No",
                    callback_data=f"love|proposal|{session_id}|reject"
                )
            ],
            [
                InlineKeyboardButton(
                    "🕵 Ask Hint",
                    callback_data=f"love|proposal|{session_id}|hint"
                )
            ],
        ]
    )


# --------------------------------------------------
# ANONYMOUS CRUSH
# --------------------------------------------------

def crush_target(session_id: str):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Reveal Identity 😏",
                    callback_data=f"love|crush|{session_id}|reveal"
                )
            ],
            [
                InlineKeyboardButton(
                    "Ignore 🙈",
                    callback_data=f"love|crush|{session_id}|ignore"
                )
            ]
        ]
    )


def crush_reveal_decision(session_id: str):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Yes, Reveal Me 💫",
                    callback_data=f"love|crush|{session_id}|yes_reveal"
                )
            ],
            [
                InlineKeyboardButton(
                    "No, Keep It Secret 🔒",
                    callback_data=f"love|crush|{session_id}|no_reveal"
                )
            ]
        ]
    )


# --------------------------------------------------
# PRANK MODE
# --------------------------------------------------

def prank_final(session_id: str):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "😱 Accept",
                    callback_data=f"love|prank|{session_id}|accept"
                )
            ],
            [
                InlineKeyboardButton(
                    "😂 It’s a Prank",
                    callback_data=f"love|prank|{session_id}|prank_reveal"
                )
            ]
        ]
    )


# --------------------------------------------------
# BREAKUP MODE
# --------------------------------------------------

def breakup_confirm(session_id: str):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "💔 Confirm Breakup",
                    callback_data=f"love|breakup|{session_id}|confirm"
                )
            ],
            [
                InlineKeyboardButton(
                    "🥺 Cancel",
                    callback_data=f"love|breakup|{session_id}|cancel"
                )
            ]
        ]
    )
