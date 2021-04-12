

def serialize(data):
    """
    Serialize the data
    :param data: Object or string
    :return: serialized data
    """
    # here data is of type string and it is encoded to bytes array
    data = data.encode()
    return data


def deserialize(data):
    """
    Deserialize the data
    :param data: serialized data
    :return: data Object or string
    """
    # here data is of type bytes array and it is decoded to string
    data = data.decode()
    return data
