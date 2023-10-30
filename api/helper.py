import random
import string


def generate_random_string(length):
    # 从所有的ASCII字符中生成随机字符串
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string
