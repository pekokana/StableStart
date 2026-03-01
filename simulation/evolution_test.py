import random
import numpy as np
from sklearn.cluster import KMeans

# -----------------------------
# パラメータ
# -----------------------------
POP_SIZE = 200
GENERATIONS = 1000
ELITE_RATE = 0.3
MUTATION_RATE = 0.05
REGRESSION_FORCE = 0.02

# -----------------------------
# 初期化
# -----------------------------
population = [
    {
        "speed": random.uniform(0.4, 0.6),
        "stamina": random.uniform(0.4, 0.6)
    }
    for _ in range(POP_SIZE)
]

environment_distance = 1600

history = []

# -----------------------------
# 世代ループ
# -----------------------------
for gen in range(GENERATIONS):

    # 環境変動
    environment_distance += random.choice([-200, 0, 200])
    environment_distance = max(1200, min(2400, environment_distance))

    # 適応度計算
    for horse in population:
        fitness = (
            0.5 * horse["speed"]
            + horse["stamina"] * (environment_distance / 2400)
        )
        horse["fitness"] = fitness

    # ソート
    population.sort(key=lambda x: x["fitness"], reverse=True)

    # 上位選抜
    elites = population[:int(POP_SIZE * ELITE_RATE)]

    # 次世代生成
    new_population = []
    while len(new_population) < POP_SIZE:
        parent = random.choice(elites)

        child_speed = parent["speed"] + random.gauss(0, MUTATION_RATE)
        child_stamina = parent["stamina"] + random.gauss(0, MUTATION_RATE)

        # 平均回帰
        child_speed -= (child_speed - 0.6) * REGRESSION_FORCE
        child_stamina -= (child_stamina - 0.6) * REGRESSION_FORCE

        # 0〜1制限
        child_speed = max(0, min(1, child_speed))
        child_stamina = max(0, min(1, child_stamina))

        new_population.append({
            "speed": child_speed,
            "stamina": child_stamina
        })

    population = new_population

    # 記録
    speeds = [h["speed"] for h in population]
    staminas = [h["stamina"] for h in population]

    # クラスタ分析
    data = np.array(list(zip(speeds, staminas)))
    kmeans = KMeans(n_clusters=3, n_init=10)
    kmeans.fit(data)

    history.append({
        "gen": gen,
        "avg_speed": np.mean(speeds),
        "avg_stamina": np.mean(staminas),
        "var_speed": np.var(speeds),
        "var_stamina": np.var(staminas),
        "clusters": len(set(kmeans.labels_)),
        "env": environment_distance
    })

# -----------------------------
# 結果表示
# -----------------------------
print("最終世代平均")
print("Speed:", history[-1]["avg_speed"])
print("Stamina:", history[-1]["avg_stamina"])
print("Speed分散:", history[-1]["var_speed"])
print("Stamina分散:", history[-1]["var_stamina"])