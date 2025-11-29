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
        }
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
