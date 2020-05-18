import os, time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Poll
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, PollHandler
import telegram

from conversation.flow_manager import *

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def button(update, context):
    logging.info(f'button {update}')
    """Send a message when the command /help is issued."""
    query = update.callback_query
    logging.info(f'query {query}')

    # query.edit_message_text(text=query.data)
    process(update, context, next(query.data))


def echo(update, context):
    """Echo the user message."""
    logging.info(update)

    responses = []

    responses.append(TextMessage(say_hi()))
    responses.append(TextMessage(say_correct()))
    responses.append(MultiItems("Choose your level", ["Easy", "Medium", "Difficult"]))

    # process(update,context,responses)
    process(update, context, next(get_text(update)))


    #send_question(update, context)


def send_question(update, context, response):
    logging.info(f'send_question {response}')
    add_typing(context)

    questions = ["1", "2", "4", "20"]
    # message = update.effective_message.reply_poll("How many eggs do you need for a cake?",
    #                                               questions, type=Poll.QUIZ, correct_option_id=2)
    # context.bot.send_poll(chat_id=931365322, question="How many eggs do you need for a cake?",
    #                       options=questions, type=Poll.QUIZ, correct_option_id=2)
    context.bot.send_poll(chat_id=931365322, question=response.question,
                          options=response.answers, type=Poll.QUIZ, correct_option_id=response.correct_answer)

    # Save some info about the poll the bot_data for later use in receive_quiz_answer
    # payload = {message.poll.id: {"chat_id": update.effective_chat.id,
    #                              "message_id": message.message_id}}
    # context.bot_data.update(payload)
    # logging.info(f'payload {payload}')
    logging.info(f'update {update}')


def process(update, context, responses):
    logging.info(f"update {update}")
    logging.info(f"update {type(update)}")

    for response in responses:
        logging.info(f"response {response}")
        logging.info(f"response {type(response)}")
        add_typing(context)
        if type(response) is TextMessage:
            add_text_message(update, context, response.message)
        elif type(response) is MultiItems:
            add_suggested_actions(update, context, response)
        elif type(response) is QuizQuestion:
            send_question(update, context, response)


def add_typing(context):
    context.bot.send_chat_action(chat_id=931365322, action=telegram.ChatAction.TYPING, timeout=1)
    time.sleep(2)


def add_text_message(update, context, message):
    context.bot.send_message(chat_id=931365322, text=message)
    # if update.message is not None:
    #     update.message.reply_text(message)
    # else:
    #     update.callback_query.edit_message_text(text=message)


def add_suggested_actions(update, context, response):
    options = []

    for item in response.items:
        options.append(InlineKeyboardButton(item, callback_data=item))

    logging.info(f"options {options}")

    reply_markup = InlineKeyboardMarkup([options])

    context.bot.send_message(chat_id=931365322, text=response.message, reply_markup=reply_markup)

    # if update.message is not None:
    #     update.message.reply_text(response.message, reply_markup=reply_markup)
    # else:
    #     update.callback_query.edit_message_text(text=response.message, reply_markup=reply_markup)


def quiz(update, context):
    logging.info(f'context {context}')


def receive_quiz_answer(update, context):
    logging.info(f'receive_quiz_answer {context.bot_data}')
    # logging.info(f'context {context.chat_data}')
    # logging.info(f'context {context.user_data}')

    logging.info(f'update {update}')
    logging.info(f'correct_option_id {update.poll.correct_option_id}')
    logging.info(f'question {update.poll.question}')
    logging.info(f'options {update.poll.options}')
    #quiz_data = context.bot_data[update.poll.id]
    # logging.info(f'quiz_data {quiz_data}')
    # logging.info(f'quiz_data["message_id"] {quiz_data["message_id"]}')
    send_question(update, context)


def get_text(update):
    return update.message.text


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(DefaultConfig.TELEGRAM_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    dp.add_handler(CommandHandler('quiz', quiz))
    dp.add_handler(PollHandler(receive_quiz_answer, pass_update_queue=True, pass_job_queue=True,
                               pass_user_data=True, pass_chat_data=True))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

class DefaultConfig:
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")


if __name__ == '__main__':
    main()