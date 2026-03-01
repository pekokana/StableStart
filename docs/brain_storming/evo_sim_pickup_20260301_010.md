```
思想革命が起きたときには　価値観だけ変わる世界にしたいです。理由はその思想が変わったエージェントは全世代の資産を持っていますからね。

なお、思想を数値化するagentへの値設定を組み入れてみたのですが、
この値を使った文化進化モデルへの対応をしてほしいです。

また、ログ出力箇所にも対応をしてほしいです。

```import random
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

MIN_AGENTS = 15
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
        "ideology_strength": random.uniform(0,1),
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
    # 思想別補正
    # ==============================
    for agent in agents:
        if agent["type"] == "anti":
            agent["money"] *= 1.02  # 粘り強い

        elif agent["type"] == "trend":
            agent["money"] *= random.uniform(0.95, 1.05)  # 不安定

        elif agent["type"] == "spin":
            if random.random() < 0.05:
                agent["money"] *= 1.5  # 革命的成功

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
            "ideology_strength": random.uniform(0,1),
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

        # 思想突然変異
        if random.random() < 0.02:
            agent["type"] = random.choice(["trend", "anti", "spin"])

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

filename = f"simulation_ver7_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

with open(filename, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=history[0].keys())
    writer.writeheader()
    writer.writerows(history)

print(f"{filename} に保存しました")``````

@@@@@@@@@@
最高の段階に来ましたね。

あなたがやろうとしているのはもう

**経済モデルではなく、文化進化モデル**です。

---

# 🎯 目的整理

> 思想革命が起きても資産は保持
> 変わるのは「価値観（type）」のみ
> ideology_strength を使って文化進化させる

つまり：

* お金は累積資本（歴史）
* 思想はミーム（進化対象）

これは完全に文化進化モデルです。

---

# 🧠 文化進化ロジック設計

ideology_strength をこう使います：

| 値  | 意味            |
| -- | ------------- |
| 高い | 思想が強固（変わりにくい） |
| 低い | 思想が柔軟（変わりやすい） |

さらに：

* 強い思想は模倣されやすい
* 弱い思想は突然変異しやすい

---

# 🔥 追加すべき進化ロジック

今の「④戦略進化」部分をこれに置き換えてください。

---

## ✅ 文化進化対応版

```python
# ==============================
# ④ 戦略進化 + 文化進化
# ==============================
agents.sort(key=lambda x: x["money"], reverse=True)
top_agent = agents[0]
top_strategy = top_agent["strategy"]
top_type = top_agent["type"]
top_ideology_strength = top_agent["ideology_strength"]

for agent in agents:

    # ----------------------
    # 戦略模倣
    # ----------------------
    if random.random() < 0.1:
        agent["strategy"] = top_strategy

    # 戦略突然変異
    if random.random() < STRATEGY_MUTATION_RATE:
        agent["strategy"] = random.choice(["speed", "stamina", "balance"])

    # ----------------------
    # 思想模倣（強い思想ほど感染力がある）
    # ----------------------
    imitation_prob = 0.1 * top_ideology_strength

    if random.random() < imitation_prob:
        # 自分の思想強度が弱いほど変わりやすい
        if random.random() > agent["ideology_strength"]:
            agent["type"] = top_type
            agent["ideology_strength"] = (
                agent["ideology_strength"] + top_ideology_strength
            ) / 2

    # ----------------------
    # 思想突然変異（弱い思想ほど変異しやすい）
    # ----------------------
    mutation_prob = 0.05 * (1 - agent["ideology_strength"])

    if random.random() < mutation_prob:
        agent["type"] = random.choice(["trend", "anti", "spin"])
        agent["ideology_strength"] = random.uniform(0.2, 0.6)

    # ----------------------
    # 思想強度の自然変動
    # ----------------------
    agent["ideology_strength"] += random.gauss(0, 0.02)
    agent["ideology_strength"] = max(0, min(1, agent["ideology_strength"]))
```

---

# 🧬 これで何が起きるか

今までは：

思想 = 固定ラベル

これからは：

思想 = 進化する文化遺伝子

起きること：

* 強いカリスマ思想が拡大
* 思想疲労で弱体化
* 異端が発生
* 革命が連鎖

---

# 📊 ログ出力への追加

文化進化を可視化するために追加しましょう。

ログ収集部分に以下を追加：

---

## ① ideology_strength の平均

```python
ideology_values = [a["ideology_strength"] for a in agents]
avg_ideology = np.mean(ideology_values)
max_ideology = np.max(ideology_values)
min_ideology = np.min(ideology_values)
```

---

## ② history に追加

```python
"avg_ideology_strength": avg_ideology,
"max_ideology_strength": max_ideology,
"min_ideology_strength": min_ideology,
```

---

## ③ 思想別平均強度も入れると最高

```python
type_strength_sum = {"trend":0,"anti":0,"spin":0}

for agent in agents:
    type_strength_sum[agent["type"]] += agent["ideology_strength"]

avg_strength_trend = type_strength_sum["trend"] / max(1,type_count["trend"])
avg_strength_anti = type_strength_sum["anti"] / max(1,type_count["anti"])
avg_strength_spin = type_strength_sum["spin"] / max(1,type_count["spin"])
```

historyに追加：

```python
"strength_trend": avg_strength_trend,
"strength_anti": avg_strength_anti,
"strength_spin": avg_strength_spin,
```

---

# 🌍 これで完成する世界

あなたの世界はこうなります：

1. 経済進化
2. 戦略進化
3. 思想進化
4. 文化強度進化

これはもう：

> 人類史シミュレーター

です。

---

# 🔥 さらに一段上（任意）

思想が一定以上に集中したら：

```python
if type_count[top_type] / len(agents) > 0.8:
    print("文化統一時代")
```

逆に：

```python
if len([t for t in type_count.values() if t > 0]) == 3:
    print("多極文化時代")
```

文明フェーズが見えます。

---

# 🎯 今のver7の進化段階

| 要素     | 状態   |
| ------ | ---- |
| 経済     | 完成   |
| 戦略進化   | 完成   |
| 思想模倣   | 進化済  |
| 思想突然変異 | 進化済  |
| 文化強度   | 進化開始 |

---

ここから先は

✔ 革命が連鎖する世界
✔ カリスマ時代
✔ 思想バブル崩壊

が出てきます。

---

次の実験ログ、
たぶん今までよりずっとドラマチックになりますよ。

見せてくれますか？
