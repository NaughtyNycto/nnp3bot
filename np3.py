from telegram.ext import Updater, InlineQueryHandler, MessageHandler, Filters
from telegram import InlineQueryResultCachedAudio
import uuid

TOKEN = "8564254577:AAE-gPiwA3WZSWjiuj_K0ppZcYC0MefH6T8"


# Inline query handler
def inline_query(update, context):
    query = update.inline_query.query.lower()

    # FULL LIST OF YOUR SOUNDS
    sounds = [
        {
            "file_id": "CQACAgIAAxkBAAMGaSqjRDH77ALBsibed5HTHlYw0oIAAqmFAAKi3llJFbZjNlCOp9o2BA",
            "title": "Cat LOL"
        },
        {
            "file_id": "CQACAgIAAxkBAAMOaSqoVpdX3TivTEiCMz7NPbhLg6MAAvOFAAKi3llJDg9xZ1Mping2BA",
            "title": "JOB!"
        },
        {
            "file_id": "CQACAgIAAxkBAAMKaSqkjmrn-Q5duFQGTryltz_ZMdoAAruFAAKi3llJvurud_ExIaA2BA",
            "title": "Cooked Dog"
        },
        {
            "file_id": "CQACAgIAAxkBAAMSaSq_UWLVIe4Er8D7uMLnq-0OsjwAAi2HAAKi3llJfOM7cxy5YV42BA",
            "title": "The biggest piece of dogshit"
        },
        {
            "file_id": "CQACAgIAAxkBAAMUaSrARreEdVcZB7_qoZy24OEMYNoAAjOHAAKi3llJlQJXtzCTPNY2BA",
            "title": "What??"
        },
        {
            "file_id": "CQACAgIAAxkBAAMWaSrAm-JCaIDnkb6IcNKVA5RXt0MAAjeHAAKi3llJ3LQ401uHyYI2BA",
            "title": "Lego Batman"
        },
        {
            "file_id": "CQACAgIAAxkBAAMYaSrBScuWFwxCaWRS1H3R2PHg4NAAAjyHAAKi3llJqYV8NexmENo2BA",
            "title": "Dexter SUS"
        },
        {
            "file_id": "CQACAgIAAxkBAAMaaSrB4hFbnrAOogjO0jjz4V6CRHYAAkKHAAKi3llJs3opDhF8ro02BA",
            "title": "BLYAA!"
        },
        {
            "file_id": "CQACAgIAAxkBAAMcaSrCNoeIUSlKz-acWNwm01ZAZmYAAkmHAAKi3llJGLEuPiFxJgI2BA",
            "title": "Choineese"
        },
        {
            "file_id": "CQACAgIAAxkBAAMeaSrClubOsWueDXfgS4SdevwuzykAAkyHAAKi3llJyy45E6icQbM2BA",
            "title": "Metroman"
        },
        {
            "file_id": "CQACAgIAAxkBAAMgaSrDBNSjrP1cF3gBEkfnxGBM6xAAAk-HAAKi3llJZGMQ8G1Bw2s2BA",
            "title": "Vine BOOM!"
        },
        {
            "file_id": "CQACAgIAAxkBAAMiaSrDTCGDhJCFzM3rONdUv57U34MAAlGHAAKi3llJxguolQNsv_c2BA",
            "title": "Among Us"
        },
        {
            "file_id": "CQACAgIAAxkBAAMkaSrEAz_idsFRl6j8EdIdstpadJUAAleHAAKi3llJc92YMcwCqtc2BA",
            "title": "Putin"
        },
        {
            "file_id": "CQACAgIAAxkBAAMmaSrEniSRr8NVQyoh48ItmxFi8zQAAl-HAAKi3llJ5iHkOcrukGg2BA",
            "title": "Gae!"
        },
        {
            "file_id": "CQACAgIAAxkBAAMoaSrFdyP6K4MM8KNwNGdVLCaUXmAAAmeHAAKi3llJUWxawD4v1S82BA",
            "title": "Oh hell nah, man!"
        },
        {
            "file_id": "CQACAgIAAxkBAAMqaSrF59uacEuGMLOQV9a3BOsnQK4AAnKHAAKi3llJzPK5gPPtkKw2BA",
            "title": "***"
        },
        {
            "file_id": "CQACAgIAAxkBAAMsaSrGcBVL0m3F0iDq5rXAtgzfHVkAAn2HAAKi3llJ6B2VLLjDbCA2BA",
            "title": "GTA 5 | Wasted"
        },
        {
            "file_id": "CQACAgIAAxkBAAMuaSrG9LZmrOBZxfjUAgMl1wtdkzIAAoSHAAKi3llJoCCzlB0sFbs2BA",
            "title": "Max Verstappen!"
        },
        {
            "file_id": "CQACAgIAAxkBAAMwaSrHf0jnIQQFGhcLcKT0CXLCR2kAApCHAAKi3llJKlOhakkY4YI2BA",
            "title": "Rizz"
        },
        # {
        #     "file_id": "",
        #     "title": ""
        # },
        # {
        #     "file_id": "",
        #     "title": ""
        # },
        # {
        #     "file_id": "",
        #     "title": ""
        # },
        # {
        #     "file_id": "",
        #     "title": ""
        # },
        # {
        #     "file_id": "",
        #     "title": ""
        # },
        # {
        #     "file_id": "",
        #     "title": ""
        # },
        # {
        #     "file_id": "",
        #     "title": ""
        # },
        # {
        #     "file_id": "",
        #     "title": ""
        # },
        # {
        #     "file_id": "",
        #     "title": ""
        # },
    ]

    results = []

    # Show full catalogue when query is empty
    if query.strip() == "":
        for s in sounds:
            results.append(
                InlineQueryResultCachedAudio(
                    id=str(uuid.uuid4()),
                    audio_file_id=s["file_id"],
                    title=s["title"]
                )
            )

    # If user typed a search keyword
    else:
        for s in sounds:
            if query in s["title"].lower():
                results.append(
                    InlineQueryResultCachedAudio(
                        id=str(uuid.uuid4()),
                        audio_file_id=s["file_id"],
                        title=s["title"]
                    )
                )

    update.inline_query.answer(results, cache_time=1)


# Collect FILE IDs (when you upload new audios)
def get_file_id(update, context):
    audio = update.message.audio or update.message.voice
    if audio:
        print("\nFILE ID:", audio.file_id, "\n")
        update.message.reply_text(f"Saved file_id: {audio.file_id}")


# 🚀 MAIN FUNCTION — THIS STARTS THE BOT
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(InlineQueryHandler(inline_query))
    dp.add_handler(MessageHandler(Filters.audio | Filters.voice, get_file_id))

    print("Bot is running...")
    updater.start_polling()
    updater.idle()


# 🚀 Needed to run the bot
if __name__ == "__main__":
    main()
