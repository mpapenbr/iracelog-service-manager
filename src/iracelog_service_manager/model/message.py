
from enum import Enum


# Note: Keep this in sync with racelogger/model/messages.py and iracelog/sotres/wamp/types.ts
class MessageType(Enum):
    EMPTY = 0
    STATE = 1
    STATE_DELTA = 2
    SPEEDMAP = 3
    CAR = 4


class Message:
    type = None
    timestamp = 0
    payload = None

    def __init__(self, type=None, payload=None) -> None:
        self.type = type
        self.payload = payload
