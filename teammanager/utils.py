import random
import string


def gen_token():
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(50))


def time_to_string(time):
    try:
        total = str(time).split(":")
        return "{}h {}m".format(total[0], total[1])
    except IndexError:
        return "0m"
