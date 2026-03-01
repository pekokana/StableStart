```
「淘汰重視モデル」>「経済循環モデル」ですが、完全に経済循環をなくしたくないです。
① 最低人口維持（例：5体以下にならない）
min_agents = 5
としつつも、再参入ではなく、新しいエージェントを生成して新規参入するようにはなりませんか？＿

実際の世界でも1000世代（1000年も生き続ける人や企業は稀ですから）

修正対象のコードはこちらになります。
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
    # 破産処理
    # ==============================
    agents = [a for a in agents if a["money"] > 0]
    if len(agents) < 2:
        break

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

    for agent in agents:
        strategy_money[agent["strategy"]] += agent["money"]
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
        "money_speed": strategy_money["speed"],
        "money_stamina": strategy_money["stamina"],
        "money_balance": strategy_money["balance"],
    })

# ==============================
# 出力
# ==============================
print("最終世代:", history[-1])

filename = f"simulation_ver4_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

with open(filename, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=history[0].keys())
    writer.writeheader()
    writer.writerows(history)

print(f"{filename} に保存しました")```

```

@@@@@
いいですね。
その思想、かなり健全です。

> ✔ 淘汰は強い
> ✔ でも完全固定世界にはしない
> ✔ 企業は死ぬ
> ✔ しかし新規参入はある

これは **進化経済モデルとして最もリアル寄り** です。

---

# 🎯 やりたいこと

現在：

```python
agents = [a for a in agents if a["money"] > 0]
if len(agents) < 2:
    break
```

これを

### ❌ 破産＝消滅＋終了

ではなく

### ✅ 破産＝消滅＋新規参入

に変更する。

さらに

### ✅ 最低人口 `min_agents = 5` を維持

---

# 🔧 修正内容

以下を **破産処理部分に置き換えてください。**

---

## ✅ ① 設定に追加

上部に追加：

```python
MIN_AGENTS = 5
NEXT_AGENT_ID = AGENTS  # 新規ID用
```

---

## ✅ ② 破産処理を置き換え

現在の破産処理を削除して、これに変更：

```python
# ==============================
# 破産処理 + 新規参入
# ==============================
global NEXT_AGENT_ID

# 生存者
agents = [a for a in agents if a["money"] > 0]

# 最低人口を維持
while len(agents) < MIN_AGENTS:

    strategy = random.choice(["speed", "stamina", "balance"])

    new_agent = {
        "id": NEXT_AGENT_ID,
        "money": INITIAL_MONEY,
        "strategy": strategy,
        "horses": [create_horse(strategy) for _ in range(HORSES_PER_AGENT)]
    }

    NEXT_AGENT_ID += 1
    agents.append(new_agent)
```

そして

```python
if len(agents) < 2:
    break
```

は **削除してください。**

---

# 🧠 これで何が起きる？

### ✔ 強者は残る

### ✔ 弱者は消える

### ✔ でも新規参入が入る

### ✔ 世界は1000世代継続する

つまり：

> 🧬 「創造的破壊モデル」

になります。

---

# 🔥 期待される挙動

1. 覇権は揺れる
2. 戦略固定しにくくなる
3. バランス戦略が必ずしも最強にならない
4. エージェント数が振動する
5. 能力天井張り付きが緩和される可能性

---

# 🎯 さらにリアルにしたいなら（任意）

新規参入を完全ランダムではなく：

### 💡 トレンド適応型にする

```python
if distance > 2000:
    strategy = random.choice(["stamina","balance"])
elif distance < 1600:
    strategy = random.choice(["speed","balance"])
else:
    strategy = random.choice(["speed","stamina","balance"])
```

これを入れると

> 🏛 市場を読んで参入する企業

になります。

---

# ⚠ 重要な副作用

今は賞金総額固定なので

新規参入が多いと：

* 資金分散
* 競争激化
* 淘汰増加

になります。

これがドラマを生みます。

---

# 🧬 あなたの世界は今

「固定世界」から

「進化市場」へ移行します。

---

次の実験後に知りたいのは：

* 覇権交代回数
* エージェント数の平均
* 能力天井張り付きの緩和有無

---

やりますか？

この変更で
StableStartは「生きた経済」になります。
