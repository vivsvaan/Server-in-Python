from enum import Enum


class MessageRequestType(Enum):
    connect = 1
    disconnect = 2
    heartbeat = 3
    message = 4


class MessageResponseType(Enum):
    connected = 1
    message = 2


class ClientStatus(Enum):
    connected = 1
    disconnected = 2
