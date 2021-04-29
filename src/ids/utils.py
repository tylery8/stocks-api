import random


def generate_random_id(length, characters=''.join(list(map(str, range(10)))), prefix="", postfix=""):
    parts = [random.choice(characters) for _ in range(length)]
    if prefix:
        parts.insert(0, prefix)
    if postfix:
        parts.append(postfix)
    return ''.join(parts)


def generate_id_for_table(table, **kwargs):
    _id = generate_random_id(**kwargs)
    while table.get_item(_id):
        _id = generate_random_id(**kwargs)
    return _id
