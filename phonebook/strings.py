# /start response
START = (
    'Welcome to <i>USPhonebook</i>, an interactive directory for module '
    'discussion telegram chat groups.'
    '\n\n'
    'For more information, please contact @ningyuan. To contribute, please '
    'visit the open source <a href="{}">GitHub repository</a>.'
).format('https://github.com/ningyuansg/module-phonebook')

# /all response
ALL_EMPTY = 'There\'s nothing to show...'

# /cancel responses
CANCEL_ALREADY_NONE = 'Okay, but you weren\'t doing anything anyways c:'
CANCEL_OK = 'Cancelled the current command!'

# /add response
ADD = 'Please enter your module code.'
ADD_INVALID_CODE = (
    'This doesn\'t seem to be a valid module code. Please try again, or use '
    '/cancel to cancel this command'
)
ADD_CODE_EXISTS = (
    'This module already has a corresponding group in the directory.'
)
ADD_PROMPT_URL = 'Now, enter the invite link.'

# response to messages by a user in states.ADD_PROMPT_URL
ADD_INVALID_URL = (
    'This doesn\'t seem to be a valid URL. Please try again, or use /cancel '
    'to cancel this command'
)
ADD_URL_EXISTS = (
    'This URL is already being used for a module in the directory.'
)
ADD_OK = (
    'All done!'
    '\n\n'
    'An entry for <code>{}</code> has been added with invite link {}'
)

# responses to using private-message-only commands in non-private-messages
PRIVATE_MESSAGES_ONLY = (
    'Oops, the command {} will only work over pm!'
)

def strfgroup(group):
    pretty_code = '<code>{:9}</code>'.format(group.code)
    pretty_link = '<a href="{}">Invite link</a>'.format(group.url)
    return '{}\u2014  {}'.format(pretty_code, pretty_link)
