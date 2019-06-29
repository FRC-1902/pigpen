import random
import string


def gen_token():
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(50))
