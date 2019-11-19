import string, random


def randomString(length: int) -> string:
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(length))

