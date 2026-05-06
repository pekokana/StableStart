import hashlib

def make_seed(text: str) -> int:
    return int(hashlib.sha256(text.encode()).hexdigest(), 16) % (10**8)

def create_seeds(user_key: str, date: str):
    global_seed = make_seed(f"{user_key}_{date}")

    return {
        "global": global_seed,
        "country": make_seed(f"{global_seed}_country"),
        "owner": make_seed(f"{global_seed}_owner"),
        "trainer": make_seed(f"{global_seed}_trainer"),
        "horse": make_seed(f"{global_seed}_horse"),
    }