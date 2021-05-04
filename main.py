import os
import requests
from pyrogram import Client, filters
from dotenv import load_dotenv
from loguru import logger

load_dotenv(os.path.join(".env"))

app = Client(
    "ultimate_pinger_bot",
    bot_token=str(os.getenv("BOT_TOKEN")),
    api_id=str(os.getenv("API_ID")),
    api_hash=str(os.getenv("API_HASH"))
)

TRUSTED_STATUS = ["creator", "administrator"]


def _can_user_ping(user, users) -> bool:
    for u in users:
        if u.user.id == user.id and u.status in TRUSTED_STATUS:
            return True


def ping_all(client, msg, *args):
    chat_user = client.get_chat_members(msg.chat.id)
    if _can_user_ping(msg.from_user, chat_user):
        mentions = [cu['user'].mention() for cu in chat_user]
        msg.reply_text(f"{' '.join(mentions)} {' '.join(args)}")
        return
    msg.reply_text("У вас нету прав так шалить")


def bot_descriprion(client, msg, *args):
    msg.reply_text(os.getenv("HELP_MSG"))


FUNCTION_HANDLER = {
    "/start": {"handler": bot_descriprion, "description": "Greetings message"},
    "/help": {"handler": bot_descriprion, "description": "Greetings message"},
    "/ping": {"handler": ping_all, "description": "Ping all chat members, usage: /ping your msg"},
}


@app.on_message(filters.command(['start', 'help', 'ping'], ["/"]))
def cmd_handler(client, message):
    parsed_msg = message.text.split(" ")
    logger.info(f"command {parsed_msg[0]} called by user {message.from_user.first_name} {message.from_user.last_name}")
    FUNCTION_HANDLER[parsed_msg[0]]["handler"](client, message, *parsed_msg[1:])


def set_bot_command():
    """ Set command description """
    set_my_command_route = f"https://api.telegram.org/bot{str(os.getenv('BOT_TOKEN'))}/setMyCommands"
    r = requests.post(set_my_command_route, json={"commands": [{"command": k, "description": v['description']}
                                                  for k, v in FUNCTION_HANDLER.items()]})
    if r.status_code != 200:
        logger.error("Can't set bot command")
        logger.debug(f"Telegram api response: {r.content}")


if __name__ == "__main__":
    set_bot_command()
    app.run()
