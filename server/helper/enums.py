from enum import Enum


class MessageRequestType(Enum):
    """
    Messages which client will send to server
    """
    connect = 1
    disconnect = 2
    heartbeat = 3
    message = 4


class MessageResponseType(Enum):
    """
    Messages which server will send to client
    """
    connected = 1
    message = 2


class ClientStatus(Enum):
    """
    Status of the client
    """
    connected = 1
    disconnected = 2
