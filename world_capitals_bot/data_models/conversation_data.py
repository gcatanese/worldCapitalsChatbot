class ConversationData:
    def __init__(
            self,
            timestamp: str = None,
            channel_id: str = None,
    ):
        self.timestamp = timestamp
        self.channel_id = channel_id

    def __str__(self):
        return f"channel_id:{self.channel_id} "
