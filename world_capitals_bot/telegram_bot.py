import os, time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Poll
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, PollHandler
import telegram

from conversation.flow_manager import *

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def get_chat_id(update):
    chat_id = -1

    if update.message is not None:
        chat_id = update.message.chat.id
    elif update.callback_query.message is not None:
        chat_id = update.callback_query.message.chat.id

    logging.info(f"chat_id {chat_id}")

    return chat_id


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def suggested_actions_handler(update, context):
    query = update.callback_query
    logging.info(f'suggested_actions choice: {query}')

    flow_manager = FlowManager()
    process(update, context, flow_manager.next(query.data))


def message_handler(update, context):
    text = get_text(update)
    logging.info(f"User says {text}")

    flow_manager = FlowManager()
    process(update, context, flow_manager.next(text))


def process(update, context, responses):
    logging.info(f"update {update}")
    logging.info(f"context {context}")

    for response in responses:
        add_typing(update, context)
        if type(response) is TextMessage:
            add_text_message(update, context, response.message)
        elif type(response) is MultiItems:
            add_suggested_actions(update, context, response)
        elif type(response) is QuizQuestion:
            add_quiz_question(update, context, response)


def add_typing(update, context):
    context.bot.send_chat_action(chat_id=get_chat_id(update), action=telegram.ChatAction.TYPING, timeout=1)
    time.sleep(2)


def add_text_message(update, context, message):
    context.bot.send_message(chat_id=get_chat_id(update), text=message)


def add_suggested_actions(update, context, response):
    options = []

    for item in response.items:
        options.append(InlineKeyboardButton(item, callback_data=item))

    reply_markup = InlineKeyboardMarkup([options])

    context.bot.send_message(chat_id=get_chat_id(update), text=response.message, reply_markup=reply_markup)


def add_quiz_question(update, context, response):
    logging.info(f'add_quiz_question {response}')

    questions = ["1", "2", "4", "20"]
    # message = update.effective_message.reply_poll("How many eggs do you need for a cake?",
    #                                               questions, type=Poll.QUIZ, correct_option_id=2)
    # context.bot.send_poll(chat_id=931365322, question="How many eggs do you need for a cake?",
    #                       options=questions, type=Poll.QUIZ, correct_option_id=2)
    context.bot.send_poll(chat_id=get_chat_id(update), question=response.question,
                          options=response.answers, type=Poll.QUIZ, correct_option_id=response.correct_answer)

    # Save some info about the poll the bot_data for later use in receive_quiz_answer
    payload = {message.poll.id: {"chat_id": update.effective_chat.id,
                                  "message_id": message.message_id}}
    # context.bot_data.update(payload)
    # logging.info(f'payload {payload}')
    logging.info(f'update {update}')


def receive_quiz_answer(update, context):
    # logging.info(f'receive_quiz_answer {context.bot_data}')
    # logging.info(f'context {context.chat_data}')
    # logging.info(f'context {context.user_data}')

    # logging.info(f'update {update}')
    # logging.info(f'correct_option_id {update.poll.correct_option_id}')
    # logging.info(f'question {update.poll.question}')
    # logging.info(f'options {update.poll.options}')
    # quiz_data = context.bot_data[update.poll.id]
    # logging.info(f'quiz_data {quiz_data}')
    # logging.info(f'quiz_data["message_id"] {quiz_data["message_id"]}')
    # send_question(update, context)

    flow_manager = FlowManager()

    process(update, context, flow_manager.next('aa'))


def get_text(update):
    return update.message.text


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" ', update)
    logger.warning('Error "%s"', context.error)


def main():
    updater = Updater(DefaultConfig.TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher

    # cmd
    dp.add_handler(CommandHandler("help", help))

    #
    dp.add_handler(PollHandler(receive_quiz_answer, pass_update_queue=True, pass_job_queue=True,
                                pass_user_data=True, pass_chat_data=True))
    # quiz answer handler
    #dp.add_handler(PollHandler(receive_quiz_answer))
    # suggested_actions_handler
    updater.dispatcher.add_handler(CallbackQueryHandler(suggested_actions_handler))
    # message handler
    dp.add_handler(MessageHandler(Filters.text, message_handler))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()


class DefaultConfig:
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")


if __name__ == '__main__':
    main()
