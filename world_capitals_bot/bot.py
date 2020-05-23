import time
from datetime import datetime

from botbuilder.core import ActivityHandler, TurnContext, MessageFactory, ConversationState, UserState
from botbuilder.schema import ChannelAccount, Activity, ActivityTypes, CardAction, SuggestedActions, ActionTypes

import logging

from conversation.flow_manager import FlowManager
from conversation._model import *
from conversation._utterance import *

from metrics.bot_metrics_connector import *

from data_models import ConversationData, UserProfile

CHANNEL = 'msbot'


def list_cards(items):
    cards = []

    for item in items:
        cards.append(CardAction(title=item, type=ActionTypes.im_back, value=item))

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


def add_quiz_question(activities, response):
    suggested_actions = MessageFactory.suggested_actions(actions=list_cards(response.answers), text=response.question)
    activities.append(suggested_actions)


def process(responses):
    activities = []

    for response in responses:
        add_typing(activities)
        if type(response) is TextMessage:
            add_text_message(activities, response)
        elif type(response) is MultiItems:
            add_suggested_actions(activities, response)
        elif type(response) is QuizQuestion:
            add_quiz_question(activities, response)

    return activities


def get_platform(turn_context):
    platform = ""

    try:
        platform = turn_context.activity.channel_id
    except Exception as error:
        logging.error(error)

    return platform


class MyBot(ActivityHandler):
    def __init__(self, conversation_state: ConversationState, user_state: UserState):
        if conversation_state is None:
            raise TypeError(
                "[StateManagementBot]: Missing parameter. conversation_state is required but None was given"
            )
        if user_state is None:
            raise TypeError(
                "[StateManagementBot]: Missing parameter. user_state is required but None was given"
            )

        self.conversation_state = conversation_state
        self.user_state = user_state

        self.conversation_data_accessor = self.conversation_state.create_property(
            "ConversationData"
        )
        self.user_profile_accessor = self.user_state.create_property("UserProfile")

    @staticmethod
    def get_input(turn_context):
        text = turn_context.activity.text

        logging.info(f'conversationId {turn_context.activity.conversation.id}')
        logging.info(f'recipient.id {turn_context.activity.recipient.id}')
        logging.info(f'recipient.name {turn_context.activity.recipient.name}')

        if text is not None:
            logging.info(f'Users says {text}')
            send_metrics(text, 'Beppe', get_platform(turn_context))

        return text

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        await self.conversation_state.save_changes(turn_context)
        await self.user_state.save_changes(turn_context)

    async def on_message_activity(self, turn_context: TurnContext):

        # Get the state properties from the turn context.
        user_profile = await self.user_profile_accessor.get(turn_context, UserProfile)
        conversation_data = await self.conversation_data_accessor.get(turn_context, ConversationData)

        # Add message details to the conversation data.
        conversation_data.timestamp = self.__datetime_from_utc_to_local(turn_context.activity.timestamp)
        conversation_data.channel_id = get_platform(turn_context)

        text = MyBot.get_input(turn_context)

        flow_manager = FlowManager(turn_context.activity.conversation.id, CHANNEL)

        activities = process(flow_manager.next(text))

        await turn_context.send_activities(activities)

    async def on_members_added_activity(
            self,
            members_added: ChannelAccount,
            turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(say_welcome())

    def __datetime_from_utc_to_local(self, utc_datetime):
        now_timestamp = time.time()
        offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(
            now_timestamp
        )
        result = utc_datetime + offset
        dd = result.strftime("%I:%M:%S %p, %A, %B %d of %Y")

        return dd
