import random
import numpy as np
import math
import csv
import datetime

# ==============================
# 設定
# ==============================
AGENTS = 20
HORSES_PER_AGENT = 10
GENERATIONS = 1000
INITIAL_MONEY = 1_000_000
TOTAL_PRIZE = 1_000_000

MUTATION = 0.05
MONSTER_RATE = 0.003
BREEDING_COST_PER_HORSE = 20000

STRATEGY_MUTATION_RATE = 0.05
DECAY_RATE = 0.995

MIN_AGENTS = 5
NEXT_AGENT_ID = AGENTS  # 新規ID用

# ==============================
# エージェント初期化
# ==============================
agents = []

for i in range(AGENTS):
    strategy = random.choice(["speed", "stamina", "balance"])
    entry_type = random.choice(["trend", "anti", "spin"])
    agents.append({
        "id": i,
        "money": INITIAL_MONEY,
        "strategy": strategy,
        "type": entry_type,
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
# トレンド初期値
# ==============================
distance = 1800

# ==============================
# ログ保存
# ==============================
history = []

# ==============================
# 世代ループ
# ==============================
for gen in range(GENERATIONS):

    # ==============================
    # ① 三層トレンド
    # ==============================

    # 長期構造波
    long_term_trend = 1800 + 200 * math.sin(gen / 300)

    # 慣性
    distance = 0.95 * distance + 0.05 * long_term_trend

    # 微ノイズ
    distance += random.uniform(-30, 30)

    # ショック
    if random.random() < 0.03:
        distance = random.choice([1200, 2400])

    distance = max(1200, min(2400, distance))

    # ==============================
    # レース評価
    # ==============================
    all_horses = []
    for agent in agents:
        for horse in agent["horses"]:
            fitness = (
                0.5 * horse["speed"]
                + horse["stamina"] * (distance / 2400)
            )
            all_horses.append((fitness, agent, horse))

    all_horses.sort(key=lambda x: x[0], reverse=True)

    # 賞金
    prizes = [0.2, 0.15, 0.1] + [0.05]*7 + [0.02]*10
    for i in range(min(20, len(all_horses))):
        prize = TOTAL_PRIZE * prizes[i]
        all_horses[i][1]["money"] += prize

    # ==============================
    # 維持費 + 繁殖コスト
    # ==============================
    for agent in agents:
        cost = sum(5000 + 3000*(h["speed"] + h["stamina"]) for h in agent["horses"])
        agent["money"] -= cost
        agent["money"] -= BREEDING_COST_PER_HORSE * HORSES_PER_AGENT


    # ==============================
    # 破産処理 + 社会的 新規参入
    # ==============================

    agents = [a for a in agents if a["money"] > 0]

    while len(agents) < MIN_AGENTS:

        entry_type = random.choice(["trend", "anti", "spin"])

        # ==========================
        # ① トレンド追随型
        # ==========================
        if entry_type == "trend":

            # 現在の覇権戦略を取得
            strategy_money = {"speed":0,"stamina":0,"balance":0}
            for a in agents:
                strategy_money[a["strategy"]] += a["money"]

            strategy = max(strategy_money, key=strategy_money.get)
            money = INITIAL_MONEY

        # ==========================
        # ② 逆張り型
        # ==========================
        elif entry_type == "anti":

            strategy_money = {"speed":0,"stamina":0,"balance":0}
            for a in agents:
                strategy_money[a["strategy"]] += a["money"]

            strategy = min(strategy_money, key=strategy_money.get)
            money = INITIAL_MONEY

        # ==========================
        # ③ 富裕層スピンオフ型
        # ==========================
        else:

            # トップ資産家を取得
            if agents:
                parent = max(agents, key=lambda x: x["money"])
                strategy = parent["strategy"]
                money = parent["money"] * 0.3  # 分家資金
            else:
                strategy = random.choice(["speed","stamina","balance"])
                money = INITIAL_MONEY

        new_agent = {
            "id": NEXT_AGENT_ID,
            "money": money,
            "strategy": strategy,
            "type": entry_type,
            "horses": [create_horse(strategy) for _ in range(HORSES_PER_AGENT)]
        }

        NEXT_AGENT_ID += 1
        agents.append(new_agent)



    # ==============================
    # ④ 戦略進化
    # ==============================
    agents.sort(key=lambda x: x["money"], reverse=True)
    top_strategy = agents[0]["strategy"]

    for agent in agents:
        # 模倣進化
        if random.random() < 0.1:
            agent["strategy"] = top_strategy

        # 突然変異
        if random.random() < STRATEGY_MUTATION_RATE:
            agent["strategy"] = random.choice(["speed", "stamina", "balance"])

        # 思想進化
        if random.random() < 0.05:
            agent["type"] = agents[0]["type"]

    # ==============================
    # 繁殖
    # ==============================
    for agent in agents:
        elites = sorted(agent["horses"],
                        key=lambda h: 0.5*h["speed"] + h["stamina"]*(distance/2400),
                        reverse=True)[:5]

        new_horses = []
        while len(new_horses) < HORSES_PER_AGENT:
            parent = random.choice(elites)

            speed = parent["speed"] + random.gauss(0, MUTATION)
            stamina = parent["stamina"] + random.gauss(0, MUTATION)

            # 怪物
            if random.random() < MONSTER_RATE:
                speed += 0.25
                stamina += 0.25

            # ② 能力自然減衰
            speed *= DECAY_RATE
            stamina *= DECAY_RATE

            speed = max(0, min(1, speed))
            stamina = max(0, min(1, stamina))

            new_horses.append({"speed": speed, "stamina": stamina})

        agent["horses"] = new_horses

    # ==============================
    # ログ収集
    # ==============================
    speeds = []
    staminas = []

    strategy_money = {"speed":0,"stamina":0,"balance":0}
    type_money = {"trend":0,"anti":0,"spin":0}
    type_count = {"trend":0,"anti":0,"spin":0}

    for agent in agents:
        strategy_money[agent["strategy"]] += agent["money"]

        type_money[agent["type"]] += agent["money"]
        type_count[agent["type"]] += 1

        for horse in agent["horses"]:
            speeds.append(horse["speed"])
            staminas.append(horse["stamina"])

    speed_type = sum(1 for s,st in zip(speeds,staminas) if s > st+0.1)
    stamina_type = sum(1 for s,st in zip(speeds,staminas) if st > s+0.1)
    balance_type = len(speeds) - speed_type - stamina_type

    history.append({
        "gen": gen,
        "agents": len(agents),

        "avg_speed": np.mean(speeds),
        "avg_stamina": np.mean(staminas),
        "trend": distance,

        "speed_ratio": speed_type/len(speeds),
        "stamina_ratio": stamina_type/len(speeds),
        "balance_ratio": balance_type/len(speeds),

        # 戦略資金
        "money_speed": strategy_money["speed"],
        "money_stamina": strategy_money["stamina"],
        "money_balance": strategy_money["balance"],

        # 思想資金
        "money_trend": type_money["trend"],
        "money_anti": type_money["anti"],
        "money_spin": type_money["spin"],

        # 思想人口
        "count_trend": type_count["trend"],
        "count_anti": type_count["anti"],
        "count_spin": type_count["spin"],
    })

# ==============================
# 出力
# ==============================
print("最終世代:", history[-1])

filename = f"simulation_ver6_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

with open(filename, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=history[0].keys())
    writer.writeheader()
    writer.writerows(history)

print(f"{filename} に保存しました")