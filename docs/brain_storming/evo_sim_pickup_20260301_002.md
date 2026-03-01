```
```import pandas as pd

# あなたのログファイル名に変更してください
filename = "simulation_log_YYYYMMDD_HHMMSS.csv"

df = pd.read_csv(filename)

print("===== ① 最終世代 =====")
print(df.iloc[-1])
print()

print("===== ② エージェント数が最小の世代 =====")
min_agents = df["agents"].min()
print(df[df["agents"] == min_agents].iloc[0])
print()

print("===== ③ トレンド最大（長距離ピーク） =====")
print(df.loc[df["trend"].idxmax()])
print()

print("===== ④ トレンド最小（短距離ピーク） =====")
print(df.loc[df["trend"].idxmin()])
print()

print("===== ⑤ 平均能力最大世代 =====")
df["avg_total"] = df["avg_speed"] + df["avg_stamina"]
print(df.loc[df["avg_total"].idxmax()])
print()

print("===== ⑥ 覇権戦略が変わった世代 =====")
prev_top = None
for i,row in df.iterrows():
    money = {
        "speed": row["money_speed"],
        "stamina": row["money_stamina"],
        "balance": row["money_balance"],
    }
    top = max(money, key=money.get)
    if prev_top is not None and top != prev_top:
        print("世代:", int(row["gen"]), "→ 覇権:", top)
    prev_top = top```このコードに「「10世代ごとのスナップショット」

print(df[df["gen"] % 100 == 0])

これで100世代ごと表示。」を追加するとどのようなコードになるのですか？

また、この結果をピックアップログファイルに保存したいです。
```

@@@@@@@@@

良い流れです 👍
では、

1. 🔎 100世代ごとのスナップショット追加
2. 📁 抽出結果を「ピックアップログ」に保存

を両方対応した完成版コードを出します。

---

# ✅ 完成版：抽出＋保存コード

```python
import pandas as pd

# ==============================
# ログ読み込み
# ==============================
filename = "simulation_log_YYYYMMDD_HHMMSS.csv"  # ←変更してください
df = pd.read_csv(filename)

# 保存用リスト
picked_rows = []

print("===== ① 最終世代 =====")
final_row = df.iloc[-1]
print(final_row)
picked_rows.append(final_row)

print("\n===== ② エージェント数が最小の世代 =====")
min_agents = df["agents"].min()
min_agent_row = df[df["agents"] == min_agents].iloc[0]
print(min_agent_row)
picked_rows.append(min_agent_row)

print("\n===== ③ トレンド最大（長距離ピーク） =====")
trend_max_row = df.loc[df["trend"].idxmax()]
print(trend_max_row)
picked_rows.append(trend_max_row)

print("\n===== ④ トレンド最小（短距離ピーク） =====")
trend_min_row = df.loc[df["trend"].idxmin()]
print(trend_min_row)
picked_rows.append(trend_min_row)

print("\n===== ⑤ 平均能力最大世代 =====")
df["avg_total"] = df["avg_speed"] + df["avg_stamina"]
max_ability_row = df.loc[df["avg_total"].idxmax()]
print(max_ability_row)
picked_rows.append(max_ability_row)

print("\n===== ⑥ 覇権戦略が変わった世代 =====")
prev_top = None
for i, row in df.iterrows():
    money = {
        "speed": row["money_speed"],
        "stamina": row["money_stamina"],
        "balance": row["money_balance"],
    }
    top = max(money, key=money.get)
    if prev_top is not None and top != prev_top:
        print("世代:", int(row["gen"]), "→ 覇権:", top)
        picked_rows.append(row)
    prev_top = top

print("\n===== ⑦ 100世代ごとのスナップショット =====")
snapshot_df = df[df["gen"] % 100 == 0]
print(snapshot_df)

for _, row in snapshot_df.iterrows():
    picked_rows.append(row)

# ==============================
# 重複除去して保存
# ==============================
picked_df = pd.DataFrame(picked_rows)
picked_df = picked_df.drop_duplicates(subset=["gen"])

output_filename = "picked_simulation_log.csv"
picked_df.to_csv(output_filename, index=False)

print(f"\n抽出ログを {output_filename} に保存しました")
```

---

# 🎯 これで何が保存される？

`picked_simulation_log.csv` には：

* 最終世代
* エージェント最小世代
* トレンド最大/最小
* 能力最大
* 覇権交代世代
* 100世代ごとのスナップショット

がまとめて保存されます。

---

# 🔬 さらに研究者向け改良（おすすめ）

もし「覇権交代世代だけ別ファイル」にしたいなら：

```python
transition_df = picked_df[picked_df["gen"].isin(
    [int(row["gen"]) for row in picked_rows]
)]
```

なども可能。

---

# 🧠 なぜこれが重要か

1000行よりも：

* 極値
* 崩壊点
* 転換点
* 定点観測

の方が進化構造を理解できます。

---

次にそのピックアップログを貼ってください。

そこから：

* 時代循環の有無
* 戦略進化の安定性
* 経済の集中度
* 能力の天井張り付き現象

を解析します。

StableStart、完全に「人工進化経済実験」になっています。
