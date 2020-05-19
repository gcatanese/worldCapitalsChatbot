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
    elif update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    elif update.poll is not None:
        chat_id = 931365322

    return chat_id


def help_command_handler(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Test your knowledge of world capitals 🌎 Say Hi to start!')


def main_handler(update, context):
    #logging.info(f'main_handler : {update}')

    flow_manager = FlowManager()

    if update.message is not None:
        process(update, context, flow_manager.next(get_text(update)))
    elif update.callback_query is not None:
        process(update, context, flow_manager.next(update.callback_query.data))
    elif update.poll is not None:
        process(update, context, flow_manager.next(get_answer(update)))


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
    message = context.bot.send_poll(chat_id=get_chat_id(update), question=response.question,
                                    options=response.answers, type=Poll.QUIZ,
                                    correct_option_id=response.correct_answer_position)

    # Save some info about the poll the bot_data for later use in receive_quiz_answer
    # payload = {message.poll.id: {"chat_id": update.effective_chat.id,
    #                              "message_id": message.message_id}}
    # context.bot_data.update(payload)


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
    logger.warning('Update "%s" ', update)
    logger.exception(context.error)


def main():
    updater = Updater(DefaultConfig.TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher

    # cmd
    dp.add_handler(CommandHandler("help", help_command_handler))

    # quiz answer handler
    dp.add_handler(PollHandler(main_handler, pass_update_queue=True, pass_job_queue=True,
                               pass_user_data=True, pass_chat_data=True))
    # suggested_actions_handler
    updater.dispatcher.add_handler(CallbackQueryHandler(main_handler))
    # message handler
    dp.add_handler(MessageHandler(Filters.text, main_handler))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    #updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",
                          port=int(DefaultConfig.PORT),
                          url_path=DefaultConfig.TELEGRAM_TOKEN)
    updater.bot.setWebhook('https://worldcapitalschatbot.herokuapp.com/' + DefaultConfig.TELEGRAM_TOKEN)

    updater.idle()


class DefaultConfig:
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
    PORT = os.environ.get("PORT", 8080)


if __name__ == '__main__':
    main()
