import pandas as pd
import datetime

# ==============================
# ログ読み込み
# ==============================
filename = "simulation_ver6_log_20260302_004255.csv"  # ←変更
df = pd.read_csv(filename)

picked_rows = []
report_lines = []  # ← print内容保存用

def log_print(text=""):
    print(text)
    report_lines.append(str(text))

# ==============================
# ① 最終世代
# ==============================
log_print("===== ① 最終世代 =====")
final_row = df.iloc[-1]
log_print(final_row)
picked_rows.append(final_row)

# ==============================
# ② エージェント数最小
# ==============================
log_print("\n===== ② エージェント数が最小の世代 =====")
min_agents = df["agents"].min()
min_agent_row = df[df["agents"] == min_agents].iloc[0]
log_print(min_agent_row)
picked_rows.append(min_agent_row)

# ==============================
# ③ トレンド最大
# ==============================
log_print("\n===== ③ トレンド最大（長距離ピーク） =====")
trend_max_row = df.loc[df["trend"].idxmax()]
log_print(trend_max_row)
picked_rows.append(trend_max_row)

# ==============================
# ④ トレンド最小
# ==============================
log_print("\n===== ④ トレンド最小（短距離ピーク） =====")
trend_min_row = df.loc[df["trend"].idxmin()]
log_print(trend_min_row)
picked_rows.append(trend_min_row)

# ==============================
# ⑤ 平均能力最大
# ==============================
log_print("\n===== ⑤ 平均能力最大世代 =====")
df["avg_total"] = df["avg_speed"] + df["avg_stamina"]
max_ability_row = df.loc[df["avg_total"].idxmax()]
log_print(max_ability_row)
picked_rows.append(max_ability_row)

# ==============================
# ⑥ 覇権戦略革命
# ==============================
log_print("\n===== ⑥ 覇権戦略が変わった世代 =====")
prev_top = None

for _, row in df.iterrows():
    money = {
        "speed": row["money_speed"],
        "stamina": row["money_stamina"],
        "balance": row["money_balance"],
    }
    top = max(money, key=money.get)

    if prev_top is not None and top != prev_top:
        log_print(f"世代: {int(row['gen'])} → 戦略革命: {top}")
        picked_rows.append(row)

    prev_top = top

# ==============================
# ⑦ 思想勝者
# ==============================
log_print("\n===== ⑦ どの思想が勝ったか =====")

prev_type = None
for _, row in df.iterrows():
    money = {
        "trend": row["money_trend"],
        "anti": row["money_anti"],
        "spin": row["money_spin"],
    }
    top = max(money, key=money.get)

    if prev_type is not None and top != prev_type:
        log_print(f"世代: {int(row['gen'])} → 思想革命: {top}")
        picked_rows.append(row)

    prev_type = top

# ==============================
# ⑧ 100世代ごと
# ==============================
log_print("\n===== ⑧ 100世代ごとのスナップショット =====")
snapshot_df = df[df["gen"] % 100 == 0]
log_print(snapshot_df)

for _, row in snapshot_df.iterrows():
    picked_rows.append(row)

# ==============================
# 重複除去してCSV保存
# ==============================
picked_df = pd.DataFrame(picked_rows)
picked_df = picked_df.drop_duplicates(subset=["gen"])

output_csv = f"picked_{filename}"
picked_df.to_csv(output_csv, index=False)

# ==============================
# テキストレポート保存
# ==============================
report_filename = f"report_{filename.replace('.csv','.txt')}"
with open(report_filename, "w", encoding="utf-8") as f:
    for line in report_lines:
        f.write(str(line) + "\n")

log_print(f"\n抽出CSV: {output_csv}")
log_print(f"分析レポート: {report_filename}")