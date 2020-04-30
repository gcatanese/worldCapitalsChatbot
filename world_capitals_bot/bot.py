# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
from enum import Enum
import logging

def get_event(self, text):
    event = None

    if is_greet_event(text):
        event = Event.GREET

    return event


def is_game_on(self, text):
    l = ['game on', 'lets start', 'lets go']

    return text.lower() in l


def is_greet_event(self, text):
    l = ['hi', 'hello', 'good day']

    return text.lower() in l


class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    @staticmethod
    def get_input(turn_context):
        text = turn_context.activity.text

        logging.info(f'input: {text}')

        return text

    async def on_message_activity(self, turn_context: TurnContext):

        text = MyBot.get_input(turn_context)

        event = get_event(text)

        await turn_context.send_activity(f"You said '{text}'")

    async def on_members_added_activity(
            self,
            members_added: ChannelAccount,
            turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")


class Event(Enum):
    GREET = 1
    GAME_ON = 2
    GAME_OVER = 3
    BYE = 4
