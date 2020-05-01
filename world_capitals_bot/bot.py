# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount, Activity, ActivityTypes
from time import sleep
import logging
from conversation.flow_manager import next


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
                text=response
            )
        ])

    async def on_members_added_activity(
            self,
            members_added: ChannelAccount,
            turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")



