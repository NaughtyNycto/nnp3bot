import logging
import os
import uuid

from telegram import (
    InlineQueryResultCachedAudio,
    InlineQueryResultArticle,
    InputTextMessageContent,
    Update,
)
from telegram.ext import (
    Updater,
    InlineQueryHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)
from telegram.error import BadRequest


# ========================
#  Logging
# ========================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ========================
#  DATA
# ========================

SOUNDS = [
    {"file_id": "CQACAgIAAxkBAAMGaSqjRDH77ALBsibed5HTHlYw0oIAAqmFAAKi3llJFbZjNlCOp9o2BA", "title": "Cat LOL"},
    {"file_id": "CQACAgIAAxkBAAMOaSqoVpdX3TivTEiCMz7NPbhLg6MAAvOFAAKi3llJDg9xZ1Mping2BA", "title": "JOB!"},
    {"file_id": "CQACAgIAAxkBAAMKaSqkjmrn-Q5duFQGTryltz_ZMdoAAruFAAKi3llJvurud_ExIaA2BA", "title": "Cooked Dog"},
    {"file_id": "CQACAgIAAxkBAAMSaSq_UWLVIe4Er8D7uMLnq-0OsjwAAi2HAAKi3llJfOM7cxy5YV42BA", "title": "The biggest piece of dogshit"},
    {"file_id": "CQACAgIAAxkBAAMUaSrARreEdVcZB7_qoZy24OEMYNoAAjOHAAKi3llJlQJXtzCTPNY2BA", "title": "What??"},
    {"file_id": "CQACAgIAAxkBAAMWaSrAm-JCaIDnkb6IcNKVA5RXt0MAAjeHAAKi3llJ3LQ401uHyYI2BA", "title": "Lego Batman"},
    {"file_id": "CQACAgIAAxkBAAMYaSrBScuWFwxCaWRS1H3R2PHg4NAAAjyHAAKi3llJqYV8NexmENo2BA", "title": "Dexter SUS"},
    {"file_id": "CQACAgIAAxkBAAMaaSrB4hFbnrAOogjO0jjz4V6CRHYAAkKHAAKi3llJs3opDhF8ro02BA", "title": "BLYAA!"},
    {"file_id": "CQACAgIAAxkBAAMcaSrCNoeIUSlKz-acWNwm01ZAZmYAAkmHAAKi3llJGLEuPiFxJgI2BA", "title": "Choineese"},
    {"file_id": "CQACAgIAAxkBAAMeaSrClubOsWueDXfgS4SdevwuzykAAkyHAAKi3llJyy45E6icQbM2BA", "title": "Metroman"},
    {"file_id": "CQACAgIAAxkBAAMgaSrDBNSjrP1cF3gBEkfnxGBM6xAAAk-HAAKi3llJZGMQ8G1Bw2s2BA", "title": "Vine BOOM!"},
    {"file_id": "CQACAgIAAxkBAAMiaSrDTCGDhJCFzM3rONdUv57U34MAAlGHAAKi3llJxguolQNsv_c2BA", "title": "Among Us"},
    {"file_id": "CQACAgIAAxkBAAMkaSrEAz_idsFRl6j8EdIdstpadJUAAleHAAKi3llJc92YMcwCqtc2BA", "title": "Putin"},
    {"file_id": "CQACAgIAAxkBAAMmaSrEniSRr8NVQyoh48ItmxFi8zQAAl-HAAKi3llJ5iHkOcrukGg2BA", "title": "Gae!"},
    {"file_id": "CQACAgIAAxkBAAMoaSrFdyP6K4MM8KNwNGdVLCaUXmAAAmeHAAKi3llJUWxawD4v1S82BA", "title": "Oh hell nah, man!"},
    {"file_id": "CQACAgIAAxkBAAMqaSrF59uacEuGMLOQV9a3BOsnQK4AAnKHAAKi3llJzPK5gPPtkKw2BA", "title": "***"},
    {"file_id": "CQACAgIAAxkBAAMsaSrGcBVL0m3F0iDq5rXAtgzfHVkAAn2HAAKi3llJ6B2VLLjDbCA2BA", "title": "GTA 5 | Wasted"},
    {"file_id": "CQACAgIAAxkBAAMuaSrG9LZmrOBZxfjUAgMl1wtdkzIAAoSHAAKi3llJoCCzlB0sFbs2BA", "title": "Max Verstappen!"},
    {"file_id": "CQACAgIAAxkBAAMwaSrHf0jnIQQFGhcLcKT0CXLCR2kAApCHAAKi3llJKlOhakkY4YI2BA", "title": "Rizz"},
    {"file_id": "CQACAgIAAxkBAAM6aStDofRBu5Z6eCOI2NubikanFR4AAiKQAAKi3llJZsl3bpg4IpA2BA", "title": "Can you give me one more day?"},
    {"file_id": "CQACAgIAAxkBAANCaSv4m6Q3wsXrP4bfuGHWgYsu0twAAguMAAL58mBJvrqlmrPXpe82BA", "title": "Um, what the actual fuck you doing in my house?"},
    {"file_id": "CQACAgIAAxkBAANEaSv5Pc8PbeMugmpwGGiW62ptskMAAhqMAAL58mBJgKQk8FC_EIk2BA", "title": "What the fuck is this? (British)"},
    {"file_id": "CQACAgIAAxkBAANGaSv58NvwaTcpZ2joNLSFbZLT9ScAAh6MAAL58mBJyzGxdQeKS6o2BA", "title": "Planktone"},
    {"file_id": "CQACAgIAAxkBAANIaSv6ijn_8iFW-tzTxcnQNrP_kX0AAieMAAL58mBJeUqlBJkbGKs2BA", "title": "RDR2 | Low honor"},
    {"file_id": "CQACAgIAAxkBAANKaSv7QwOPOWZNeVRAZbs8tXIpyewAAi2MAAL58mBJJ8CzYz7lwdA2BA", "title": "It was perfect!"},
    {"file_id": "CQACAgIAAxkBAANNaSv88YYl43bD-ikjoTpe4U43-GAAAjiMAAL58mBJgpIg_pTNi3A2BA", "title": "Kurt Angle"},
    {"file_id": "CQACAgIAAxkBAANYaS9CFTmBdjWzKqFBEATNe857rrgAAhaTAALOJHhJFAABT6tD5AqnNgQ", "title": "You're goddamn right!"},
    {"file_id": "CQACAgIAAxkBAANcaS9EAAH_tv-3Y-VeOTVds2_geU7bAAIskwACziR4SXIKmJUmijFeNgQ", "title": "bokachan"},
    {"file_id": "CQACAgIAAxkBAANaaS9C543mqb1w498ySE4tnlXQ85MAAiGTAALOJHhJta4FxK8UI2o2BA", "title": "Bad to the Bone"},
    {"file_id": "CQACAgIAAxkBAANeaS9ExoXStgsgvfM55cMCbCWaJLMAAjCTAALOJHhJU6nO_28yNEM2BA", "title": "Romancee"},
    {"file_id": "CQACAgIAAxkBAANgaS9FbWUAAZ8lIhZCCwv9_QlUPEJfAAI7kwACziR4Sd_VaSN6VJ47NgQ", "title": "WTF is going on here?"},
    {"file_id": "CQACAgIAAxkBAANiaS9GDzP_RW0p6jED-ucT4h5DhqIAAkSTAALOJHhJrDCQXbSalIo2BA", "title": "You can't do this to me"},
    {"file_id": "CQACAgIAAxkBAANkaS9Gjt0MjsMvzQPb8EkAAQ9Is1HjAAJIkwACziR4SQ4O24QTHp6tNgQ", "title": "Litvin"},
    # {"file_id": "", "title": ""},
    # {"file_id": "", "title": ""},
    # {"file_id": "", "title": ""},
    # {"file_id": "", "title": ""},
    # {"file_id": "", "title": ""},
    # {"file_id": "", "title": ""},
    # {"file_id": "", "title": ""},
    # {"file_id": "", "title": ""},
    # {"file_id": "", "title": ""},
    # {"file_id": "", "title": ""},
    # {"file_id": "", "title": ""},
    # {"file_id": "", "title": ""},
    # {"file_id": "", "title": ""},
    # {"file_id": "", "title": ""},
]


# ========================
#  Inline & file-id Handlers
# ========================

def inline_query(update: Update, context: CallbackContext):
    query = (update.inline_query.query or "").strip().lower()
    results = []

    # Banner
    results.append(
        InlineQueryResultArticle(
            id="banner",
            title="Made by @NaughtyNycto",
            description="you know what?",
            thumb_url="https://raw.githubusercontent.com/NaughtyNycto/sources/main/Robloxface.jpg",
            input_message_content=InputTextMessageContent(
                'Hey! I am an <a href="https://t.me/naughtynycto">unemployed teenager</a>, '
                'who is pursuing a CS major. I hope you liked my bot.\n\n'
                '5614681253742161 - in case if you want to buy me a shawarma :)',
                parse_mode="HTML"
            ),
        )
    )

    # Filter by query
    matched = [s for s in SOUNDS if query in s["title"].lower()] if query else SOUNDS

    for s in matched:
        results.append(
            InlineQueryResultCachedAudio(
                id=str(uuid.uuid4()),
                audio_file_id=s["file_id"],
                title=s["title"],
            )
        )

    try:
        update.inline_query.answer(results, cache_time=10, is_personal=True)
    except BadRequest as e:
        if "Query is too old" in str(e):
            logger.warning("Ignored expired query.")
        else:
            logger.exception(e)


def get_file_id(update: Update, context: CallbackContext):
    audio = update.message.audio or update.message.voice
    if audio:
        update.message.reply_text(f"Saved file_id: {audio.file_id}")


def error_handler(update, context):
    logger.error(f"Error: {context.error}")


# ========================
#  START BOT (Webhook on Render, polling locally)
# ========================

def main():
    token = os.getenv("TOKEN")
    if not token:
        raise RuntimeError("TOKEN env variable missing!")

    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(InlineQueryHandler(inline_query))
    dp.add_handler(MessageHandler(Filters.audio | Filters.voice, get_file_id))
    dp.add_error_handler(error_handler)

    port = int(os.environ.get("PORT", "10000"))
    external_url = os.environ.get("RENDER_EXTERNAL_URL")

    if external_url:
        # RENDER → use webhook
        webhook_path = f"/{token}"
        webhook_url = external_url.rstrip("/") + webhook_path

        logger.info(f"Starting webhook on 0.0.0.0:{port}{webhook_path}")
        logger.info(f"Setting webhook URL to: {webhook_url}")

        updater.start_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=token,
            webhook_url=webhook_url
        )

    else:
        # Local → fallback to polling
        logger.info("Local dev mode → polling")
        updater.start_polling(drop_pending_updates=True)

    updater.idle()


if __name__ == "__main__":
    main()
