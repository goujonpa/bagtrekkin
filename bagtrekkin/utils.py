import hashlib
import random


def generate_random(n):
    return ''.join(['%s' % random.randrange(10) for i in range(n)])


def generate_token(key):
    return hashlib.sha224('%s%s%s' % (generate_random(10), key, generate_random(10))).hexdigest()
