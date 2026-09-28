import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")
def keep_alive():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from telegram.error import TelegramError

# Logging Setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Configuration Variables
BOT_TOKEN = "8788665460:AAG6l3TtMcu_zMKZoGsE0K6GuI3Xzn1AaIc"

# 15 Channels ki List
# IMPORTANT: Auto-check ke liye har channel me "id" (username jaise "@alltypeLootOffcial") hona zaroori hai.
# Saath hi Bot ko in sabhi channels me ADMIN hona zaroori hai tabhi bot check kar payega.
CHANNELS = [
    {"name": "1 ↗100₹", "url": "https://t.me/+tva1AQqyOfs0NDZl", "id": "@alltypeLootOffcial"},
    {"name": "Channel 2 ↗", "url": "https://t.me/+wDEyYF4VI0dhZGE1", "id": "@alltypeLootOffcial"},
    {"name": "Channel 3 ↗", "url": "https://t.me/+MbbHfF_1YCg4YzE1", "id": "@alltypeLootOffcial"},
    {"name": "Channel 4 ↗", "url": "https://t.me/+kImKZcdbhOJlYzdl", "id": "@alltypeLootOffcial"},
    {"name": "Channel 5 ↗", "url": "https://t.me/+Q-x-DBsZieI0ZDhl", "id": "@alltypeLootOffcial"},
    {"name": "Channel 6 ↗", "url": "https://t.me/+ENe6vDYnovo4YmM1", "id": "@alltypeLootOffcial"},
    {"name": "Channel 7 ↗", "url": "https://t.me/+qZ_4QGl6Y5tmMDhl", "id": "@alltypeLootOffcial"},
    {"name": "Channel 8 ↗", "url": "https://t.me/+-lzefXQk3X1kOWVl", "id": "@alltypeLootOffcial"},
    {"name": "Channel 9 ↗", "url": "https://t.me/+Zuiimo1yU-05MDU9", "id": "@alltypeLootOffcial"},
    {"name": "Channel 10 ↗", "url": "https://t.me/+IMzkzI4O75FkODE9", "id": "@alltypeLootOffcial"},
    {"name": "Channel 11 ↗", "url": "https://t.me/+gMhril3Ljz00Mzhl", "id": "@alltypeLootOffcial"},
    {"name": "Channel 12 ↗", "url": "https://t.me/+kBv3fm-iwoExOTE1", "id": "@alltypeLootOffcial"},
    {"name": "Channel 13 ↗", "url": "https://t.me/+0yPziIGGl1M2MDQ1", "id": "@alltypeLootOffcial"},
    {"name": "Channel 14 ↗", "url": "https://t.me/alltypeLootOffcial", "id": "@alltypeLootOffcial"},
    {"name": "Channel 15 ↗", "url": "https://t.me/alltypeLootOffcial", "id": "@alltypeLootOffcial"},
]

async def is_user_joined_all(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """
    Check karta hai ki user ne saare channels join kiye hain ya nahi.
    """
    for ch in CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=ch["id"], user_id=user_id)
            if member.status in ['left', 'kicked']:
                return False
        except TelegramError:
            # Agar bot channel me admin nahi hai ya channel ID galat hai
            pass
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Stage 1: Account Linked & 15 Channels Join Prompt
    """
    user_id = update.effective_user.id
    
    if "chances" not in context.user_data:
        context.user_data["chances"] = 0
        context.user_data["has_joined"] = False

    message_text = (
        "📢 *Account Linked Successfully!*\n\n"
        "Welcome to the *Diwa~Ace Official Bot!* 🎉\n\n"
        "📢 Join all 15 official channels below to unlock 1 free lucky draw(s).\n\n"
        "🎁 Your rewards will be delivered directly to your in-game mailbox.\n\n"
        f"🆔 *Your UID:* `{user_id}`"
    )

    # 15 channels ke buttons ko 2 columns me arrange karna
    keyboard = []
    for i in range(0, len(CHANNELS), 2):
        row = []
        row.append(InlineKeyboardButton(CHANNELS[i]["name"], url=CHANNELS[i]["url"]))
        if i + 1 < len(CHANNELS):
            row.append(InlineKeyboardButton(CHANNELS[i+1]["name"], url=CHANNELS[i+1]["url"]))
        keyboard.append(row)
    
    # Bottom par "I've Joined" button
    keyboard.append([InlineKeyboardButton("✅ I've Joined All", callback_data="verify_join")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(
            text=message_text,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    elif update.callback_query:
        await update.callback_query.message.edit_text(
            text=message_text,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id

    # Stage 2: Verification After Joining Channels
    if data == "verify_join":
        # Check karein ki user ne sabhi channels join kiye hain ya nahi
        joined = await is_user_joined_all(user_id, context)
        
        if not joined:
            await query.answer("❌ Aapne sabhi channels join nahi kiye hain! Kripya saare channels join karein.", show_alert=True)
            return

        await query.answer()
        context.user_data["has_joined"] = True
        context.user_data["chances"] = 1

        text = (
            "✅ *Channels Verified!*\n\n"
            "🎉 You've unlocked 1 lucky draw chance(s).\n\n"
            "🎰 *Total Available: 1*\n\n"
            "Tap the button below to try your luck. "
            "Any prizes you win will be sent directly to your in-game mailbox!"
        )

        keyboard = [[InlineKeyboardButton("Draw Now", callback_data="draw_now")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.edit_text(
            text=text,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    # Stage 3: Lucky Draw Result
    elif data == "draw_now":
        await query.answer()
        chances = context.user_data.get("chances", 0)

        if chances > 0:
            context.user_data["chances"] -= 1
            ref_number = "49023"

            text = (
                "🎉 *Lucky Draw Completed!*\n\n"
                f"🎟️ *Reference:* {ref_number}\n"
                f"🆔 *UID:* `{user_id}`\n"
                "🎁 *Reward:* Welcome to Diwa~Ace Robot\n\n"
                f"🎰 *Remaining Chances:* {context.user_data['chances']}\n\n"
                "Your reward has been sent to your in-game *Inbox*. Open *Diwa~Ace* to claim it."
            )

            keyboard = [
                [
                    InlineKeyboardButton("Draw Again", callback_data="draw_now"),
                    InlineKeyboardButton("Back to Menu", callback_data="back_to_menu")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.message.edit_text(
                text=text,
                parse_mode="Markdown",
                reply_markup=reply_markup
            )
        else:
            await query.answer("❌ No remaining chances available!", show_alert=True)

    elif data == "back_to_menu":
        await query.answer()
        await start(update, context)


def main():
    app = (
        ApplicationBuilder().token(BOT_TOKEN).concurrent_updates(True).build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button_click))

    print("Bot starting...")
    app.run_polling(drop_pending_updates=True, stop_signals=None)


if __name__ == "__main__":
    keep_alive()
    main()
