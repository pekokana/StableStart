import random
import numpy as np
import math

# ==============================
# 設定
# ==============================
AGENTS = 10
HORSES_PER_AGENT = 10
GENERATIONS = 1000
INITIAL_MONEY = 1_000_000
TOTAL_PRIZE = 1_000_000

MUTATION = 0.05
MONSTER_RATE = 0.003

# ==============================
# エージェント初期化
# ==============================
agents = []

for i in range(AGENTS):
    strategy = random.choice(["speed", "stamina", "balance"])
    agents.append({
        "id": i,
        "money": INITIAL_MONEY,
        "strategy": strategy,
        "horses": []
    })

def create_horse(strategy):
    base_speed = random.uniform(0.4, 0.6)
    base_stamina = random.uniform(0.4, 0.6)

    if strategy == "speed":
        base_speed += 0.1
    elif strategy == "stamina":
        base_stamina += 0.1

    return {
        "speed": min(1, base_speed),
        "stamina": min(1, base_stamina)
    }

for agent in agents:
    agent["horses"] = [create_horse(agent["strategy"]) for _ in range(HORSES_PER_AGENT)]

# ==============================
# 世代ループ
# ==============================
for gen in range(GENERATIONS):

    # --- 環境 ---
    distance = 1800 + 400 * math.sin(gen / 60)

    if random.random() < 0.05:
        distance = random.choice([1200, 2400])

    # --- 全馬リスト化 ---
    all_horses = []
    for agent in agents:
        for horse in agent["horses"]:
            fitness = (
                0.5 * horse["speed"]
                + horse["stamina"] * (distance / 2400)
            )
            all_horses.append((fitness, agent, horse))

    all_horses.sort(key=lambda x: x[0], reverse=True)

    # --- 賞金分配（上位20頭） ---
    prizes = [0.2, 0.15, 0.1] + [0.05]*7 + [0.02]*10
    for i in range(min(20, len(all_horses))):
        prize = TOTAL_PRIZE * prizes[i]
        all_horses[i][1]["money"] += prize

    # --- 維持費 ---
    for agent in agents:
        cost = 0
        for horse in agent["horses"]:
            cost += 5000 + 3000*(horse["speed"] + horse["stamina"])
        agent["money"] -= cost

    # --- 破産処理 ---
    agents.sort(key=lambda x: x["money"], reverse=True)
    agents = [a for a in agents if a["money"] > 0]

    if len(agents) < 2:
        # 最低2人維持
        while len(agents) < 2:
            agents.append({
                "id": random.randint(100,999),
                "money": INITIAL_MONEY,
                "strategy": random.choice(["speed","stamina","balance"]),
                "horses": [create_horse("balance") for _ in range(HORSES_PER_AGENT)]
            })

    # --- 繁殖 ---
    for agent in agents:
        new_horses = []
        elites = sorted(agent["horses"], 
                        key=lambda h: 0.5*h["speed"] + h["stamina"]*(distance/2400),
                        reverse=True)[:5]

        while len(new_horses) < HORSES_PER_AGENT:
            parent = random.choice(elites)

            speed = parent["speed"] + random.gauss(0, MUTATION)
            stamina = parent["stamina"] + random.gauss(0, MUTATION)

            # 怪物変異
            if random.random() < MONSTER_RATE:
                speed += 0.25
                stamina += 0.25

            speed = max(0, min(1, speed))
            stamina = max(0, min(1, stamina))

            new_horses.append({"speed": speed, "stamina": stamina})

        agent["horses"] = new_horses

# ==============================
# 最終結果
# ==============================
print("生存エージェント数:", len(agents))
for a in agents:
    print("ID:", a["id"], 
          "資金:", int(a["money"]), 
          "戦略:", a["strategy"])