def summarize_world(world):
    return [
        {
            "name": c["name"],
            "owners": len(c["owners"]),
            "trainers": len(c["trainers"]),
            "horses": len(c["horses"])
        }
        for c in world["countries"]
    ]