import random


def generate_post_code():
    return ''.join(random.choices('0123456789', k=10))


def post_code_to_first_name(s, pad=False):
    if pad and len(s) % 2:
        s += '0'
    return ''.join(chr(ord('a') + int(s[i:i + 2]) % 26) for i in range(0, len(s) - 1, 2))


def closest_name_to_mean(names):
    if not names:
        raise ValueError("Список имён пуст")

    lengths = [len(n) for n in names]
    mean = sum(lengths) / len(lengths)
    return min(names, key=lambda n: abs(len(n) - mean))
