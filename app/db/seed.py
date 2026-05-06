import hashlib
import random

def create_seed(keyword: str):
    h = hashlib.sha256(keyword.encode()).hexdigest()
    seed = int(h[:8], 16)
    random.seed(seed)
    return seed