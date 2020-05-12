from botbuilder.core import ActivityHandler, TurnContext, MessageFactory
from botbuilder.schema import ChannelAccount, Activity, ActivityTypes, CardAction, SuggestedActions, ActionTypes

import logging

from conversation.flow_manager import FlowManager
from conversation._model import *
from conversation._utterance import *

from metrics.bot_metrics_connector import *


def list_cards(items):
    cards = []

    for item in items:
        cards.append(CardAction(title=item.title, type=ActionTypes.im_back, value=item.value))

    return cards


def add_typing(activities):
    activities.append(Activity(type=ActivityTypes.typing))
    activities.append(Activity(type="delay", value=2000))

    return activities


def add_text_message(activities, response):
    activities.append(Activity(type=ActivityTypes.message, text=response.message))


def add_suggested_actions(activities, response):
    suggested_actions = MessageFactory.suggested_actions(actions=list_cards(response.items), text=response.message)
    activities.append(suggested_actions)


def process(responses):
    activities = []

    for response in responses:
        add_typing(activities)
        if type(response) is TextMessage:
            add_text_message(activities, response)
        elif type(response) is MultiItems:
            add_suggested_actions(activities, response)

    return activities


def get_platform(turn_context):
    platform = ""

    try:
        platform = turn_context.activity.channel_id
    except Exception as error:
        logging.error(error)

    return platform


class MyBot(ActivityHandler):

    @staticmethod
    def get_input(turn_context):
        text = turn_context.activity.text

        if text is not None:
            logging.info(f'Users says {text}')
            send_metrics(text, 'Beppe', get_platform(turn_context))

        return text

    async def on_message_activity(self, turn_context: TurnContext):

        text = MyBot.get_input(turn_context)

        flowManager = FlowManager()

        activities = process(flowManager.next(text))

        await turn_context.send_activities(activities)

    async def on_members_added_activity(
            self,
            members_added: ChannelAccount,
            turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(say_welcome())
