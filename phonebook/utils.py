import strings

def restrict_to_private_messages(command_handler_func):
    r"""Only allow this command to be used in private chats

    If this decorator is chained with others, the other decorators nested within
    this (placed below this decorator) will not be called if the command we are
    'processing' is from a group chat, because we will call the function
    warn_restrict_to_private_messages instead of the argument
    command_handler_func.
    """
    def checker(bot, update):
        if update.effective_chat and update.effective_chat.type == 'private':
            return command_handler_func(bot, update)
        else:
            return warn_restrict_to_private_messages(bot, update)

    return checker

def warn_restrict_to_private_messages(bot, update):
    r"""A function to be passed as a commandhandler callback. Can also be used
    in an `is` identity check in `db.record_stat` to prevent recording stats for
    bot commands that are meant for private messages only, but sent to a group
    chat.
    """
    return bot.send_message(
        chat_id=update.message.chat_id,
        text=strings.PRIVATE_MESSAGES_ONLY.format(update.message.text)
    )
