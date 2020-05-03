# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext, MessageFactory
from botbuilder.schema import ChannelAccount, Activity, ActivityTypes, CardAction, SuggestedActions, ActionTypes
from time import sleep
import logging

from conversation.multi_items_response import *

from conversation.flow_manager import next


def list_cards(items):
    cards = []

    for item in items:
        cards.append(CardAction(title=item, type=ActionTypes.im_back, value=item))

    return cards


class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    @staticmethod
    def get_input(turn_context):
        text = turn_context.activity.text

        logging.info(f'input: {text}')

        return text

    async def on_message_activity(self, turn_context: TurnContext):

        text = MyBot.get_input(turn_context)

        response = next(text)
        logging.info(response)

        if type(response) is str:
            await self.send_text_reply(response, response)
        elif isinstance(response, MultiItems):
            self.send_suggested_options_reply(response, turn_context)

    async def send_text_reply(self, reply, turn_context: TurnContext):
        await turn_context.send_activities([
            Activity(
                type=ActivityTypes.typing
            ),
            Activity(
                type="delay",
                value=2000
            ),
            Activity(
                type=ActivityTypes.message,
                text=reply
            )
        ])

    async def send_suggested_options_reply(self, response, turn_context: TurnContext):
        reply = MessageFactory.text(response.message)
        reply.suggested_actions = SuggestedActions(
            actions=[
                list_cards(response.items)
            ]
        )
        await turn_context.send_activity(reply)

    async def on_members_added_activity(
            self,
            members_added: ChannelAccount,
            turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")
