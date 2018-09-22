import logging, os
import telegram
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

import db, states, strings, utils, validate

logging.basicConfig(level=logging.DEBUG)

@db.record_stat
def start(bot, update):
    db.insert_user(update.message.chat_id)
    return bot.send_message(
        chat_id=update.message.chat_id,
        text=strings.START,
        parse_mode=telegram.ParseMode.HTML,
        disable_web_page_preview=True
    )

@db.record_stat
def _all(bot, update):
    groups = db.get_all_groups()
    if groups:
        lines = (strings.strfgroup(group) for group in groups)
        message = '\n'.join(sorted(lines))
    else:
        message = strings.ALL_EMPTY
    return bot.send_message(
        chat_id=update.message.chat_id,
        text=message,
        parse_mode=telegram.ParseMode.HTML
    )

@utils.restrict_to_private_messages
@db.record_stat
def add(bot, update):
    db.update_user_state(update.message.chat_id, states.ADD_PROMPT_CODE)
    return bot.send_message(
        chat_id=update.message.chat_id,
        text=strings.ADD
    )

@db.record_stat
def cancel(bot, update):
    user = db.get_user(update.message.chat_id)
    if user is None or user.state == states.NONE:
        # user is None if /start was not sent
        return bot.send_message(
            chat_id=user.user_id,
            text=strings.CANCEL_ALREADY_NONE
        )
    else:
        db.update_user_state(user.user_id, states.NONE)
        return bot.send_message(
            chat_id=user.user_id,
            text=strings.CANCEL_OK
        )

def handle_messages(bot, update):
    user = db.get_user(update.message.chat_id)
    if user.state == states.NONE:
        return handle_messages_state_none(bot, update)
    elif user.state == states.ADD_PROMPT_CODE:
        return handle_messages_state_add_prompt_code(bot, update)
    elif user.state == states.ADD_PROMPT_URL:
        return handle_messages_state_add_prompt_url(bot, update)
    else:
        return None

def handle_messages_state_none(bot, update):
    """When user sends a text message, but is not in a state"""
    return None

def handle_messages_state_add_prompt_code(bot, update):
    """When user sends a text message in response to the bot's prompt to send a
    module code over."""
    code = update.message.text.upper()
    user_id = update.message.chat_id
    if not validate.is_code_valid(code):
        return bot.send_message(chat_id=user_id, text=strings.ADD_INVALID_CODE)
    elif not validate.is_code_unique(code):
        return bot.send_message(chat_id=user_id, text=strings.ADD_CODE_EXISTS)
    else:
        db.update_user_state(user_id, states.ADD_PROMPT_URL)
        db.update_user_saved_state(user_id, code)
        return bot.send_message(chat_id=user_id, text=strings.ADD_PROMPT_URL)

def handle_messages_state_add_prompt_url(bot, update):
    """When user sends a text message in response to the bot's prompt to send a
    URL invite link over."""
    url = update.message.text
    user_id = update.message.chat_id
    if not validate.is_url_valid(url):
        return bot.send_message(chat_id=user_id, text=strings.ADD_INVALID_URL)
    elif not validate.is_url_unique(url):
        return bot.send_message(chat_id=user_id, text=strings.ADD_URL_EXISTS)
    else:
        user = db.get_user(user_id)
        db.insert_group(user.saved_state, url, user.user_id)
        db.update_user_state(user_id, states.NONE)
        db.update_user_saved_state(user_id, None)
        return bot.send_message(
            chat_id=user_id,
            text=strings.ADD_OK.format(user.saved_state, url),
            parse_mode=telegram.ParseMode.HTML
        )

bot = Updater(token=os.environ['TOKEN'])
bot.dispatcher.add_handler(CommandHandler('start', start))
bot.dispatcher.add_handler(CommandHandler('help', start))
bot.dispatcher.add_handler(CommandHandler('all', _all))
bot.dispatcher.add_handler(CommandHandler('add', add))
bot.dispatcher.add_handler(CommandHandler('cancel', cancel))
bot.dispatcher.add_handler(MessageHandler(Filters.text, handle_messages))
