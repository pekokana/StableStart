import pandas as pd
import datetime

# ==============================
# ログ読み込み
# ==============================
filename = "simulation_ver5_log_20260301_231516.csv"  # ←変更してください
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

output_filename = f"picked_{filename}"
# f"picked_simulation_ver4_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
picked_df.to_csv(output_filename, index=False)

print(f"\n抽出ログを {output_filename} に保存しました")