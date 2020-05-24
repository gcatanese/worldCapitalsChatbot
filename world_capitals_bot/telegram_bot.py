import os, time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Poll
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, PollHandler, \
    PollAnswerHandler
import telegram

from config import DefaultConfig
from conversation.flow_manager import *

CHANNEL = 'telegram'



def get_chat_id(update, context):
    chat_id = -1

    if update.message is not None:
        chat_id = update.message.chat.id
    elif update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    elif update.poll is not None:
        chat_id = context.bot_data[update.poll.id]

    return chat_id


def get_user(update):
    user: User = None

    _from = None

    if update.message is not None:
        _from = update.message.from_user
    elif update.callback_query is not None:
        _from = update.callback_query.from_user

    if _from is not None:
        user = User()
        user.id = _from.id
        user.first_name = _from.first_name
        user.last_name = _from.last_name
        user.lang = _from.language_code if _from.language_code is not None else 'n/a'

    logging.info(f'from {user}')

    return user


def help_command_handler(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Test your knowledge of world capitals 🌎 Say Hi to start!')


def main_handler(update, context):
    logging.info(f'update : {update}')

    flow_manager = FlowManager(get_chat_id(update, context), CHANNEL, get_user(update))

    if update.message is not None:
        process(update, context, flow_manager.next(get_text(update)))
    elif update.callback_query is not None:
        process(update, context, flow_manager.next(update.callback_query.data))
    elif update.poll is not None:
        process(update, context, flow_manager.next(get_answer(update)))
        # remove from bot_data
        del context.bot_data[update.poll.id]


def process(update, context, responses):
    for response in responses:
        add_typing(update, context)
        if type(response) is TextMessage:
            add_text_message(update, context, response.message)
        elif type(response) is MultiItems:
            add_suggested_actions(update, context, response)
        elif type(response) is QuizQuestion:
            add_quiz_question(update, context, response)


def add_typing(update, context):
    context.bot.send_chat_action(chat_id=get_chat_id(update, context), action=telegram.ChatAction.TYPING, timeout=1)
    time.sleep(0)


def add_text_message(update, context, message):
    context.bot.send_message(chat_id=get_chat_id(update, context), text=message)


def add_suggested_actions(update, context, response):
    options = []

    for item in response.items:
        options.append(InlineKeyboardButton(item, callback_data=item))

    reply_markup = InlineKeyboardMarkup([options])

    context.bot.send_message(chat_id=get_chat_id(update, context), text=response.message, reply_markup=reply_markup)


def add_quiz_question(update, context, response):
    message = context.bot.send_poll(chat_id=get_chat_id(update, context), question=response.question,
                                    options=response.answers, type=Poll.QUIZ,
                                    correct_option_id=response.correct_answer_position, is_anonymous=True,
                                    timeout=5)

    # Save some info about the poll the bot_data for later use in receive_quiz_answer
    context.bot_data.update({message.poll.id: message.chat.id})


def get_text(update):
    return update.message.text


def get_answer(update):
    answers = update.poll.options

    ret = ""

    for answer in answers:
        if answer.voter_count == 1:
            ret = answer.text

    return ret


def error(update, context):
    """Log Errors caused by Updates."""
    logging.warning('Update "%s" ', update)
    logging.exception(context.error)


def main():
    updater = Updater(DefaultConfig.TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher

    # cmd
    dp.add_handler(CommandHandler("help", help_command_handler))

    # quiz answer handler
    dp.add_handler(PollHandler(main_handler, pass_chat_data=True, pass_user_data=True))
    # suggested_actions_handler
    updater.dispatcher.add_handler(CallbackQueryHandler(main_handler, pass_chat_data=True, pass_user_data=True))
    # message handler
    dp.add_handler(MessageHandler(Filters.text, main_handler))
    # quiz answer handler
    dp.add_handler(PollHandler(main_handler))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    if DefaultConfig.MODE == 'webhook':

        updater.start_webhook(listen="0.0.0.0",
                              port=int(DefaultConfig.PORT),
                              url_path=DefaultConfig.TELEGRAM_TOKEN)
        updater.bot.setWebhook(DefaultConfig.WEBHOOK_URL + DefaultConfig.TELEGRAM_TOKEN)

        logging.info(f"Start webhook mode on port {DefaultConfig.PORT}")
    else:
        updater.start_polling()
        logging.info(f"Start polling mode")

    updater.idle()


if __name__ == '__main__':
    # Enable logging
    DefaultConfig.init_logging()

    main()
