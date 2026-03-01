import pandas as pd
import datetime

# ==============================
# ログ読み込み
# ==============================
filename = "simulation_ver8_log_20260302_014806.csv"  # ←変更
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
# AI資金 最大世代
# ==============================
log_print("\n===== AI資金 最大世代 =====")

if "ai_money" in df.columns:
    ai_max_row = df.loc[df["ai_money"].idxmax()]
    log_print(ai_max_row)
    picked_rows.append(ai_max_row)
else:
    log_print("ai_money列が存在しません")

# ==============================
# AI資金 最小世代
# ==============================
log_print("\n===== AI資金 最小世代 =====")

if "ai_money" in df.columns:
    ai_min_row = df.loc[df["ai_money"].idxmin()]
    log_print(ai_min_row)
    picked_rows.append(ai_min_row)

# ==============================
# AIが市場最大資金を超えた瞬間
# ==============================
log_print("\n===== AI覇権獲得 =====")

for _, row in df.iterrows():
    market_top = max(
        row["money_speed"],
        row["money_stamina"],
        row["money_balance"]
    )
    if row["ai_money"] >= market_top:
        log_print(f"世代 {int(row['gen'])} → AIが市場覇権級に到達")
        picked_rows.append(row)
        break

# ==============================
# AI資金急変（AIショック）
# ==============================
log_print("\n===== AI資金急変 =====")

df["ai_diff"] = df["ai_money"].diff().abs()

ai_revolution_threshold = df["ai_money"].mean() * 0.3  # 調整可

ai_shock_rows = df[df["ai_diff"] > ai_revolution_threshold]

for _, row in ai_shock_rows.iterrows():
    log_print(
        f"世代 {int(row['gen'])} → AI資金急変 Δ={row['ai_diff']:.0f}"
    )
    picked_rows.append(row)

# ==============================
# AI市場支配率ピーク世代
# ==============================
log_print("\n===== AI市場支配率ピーク世代 =====")

df["total_market_money"] = (
    df["money_speed"]
    + df["money_stamina"]
    + df["money_balance"]
)

df["ai_share"] = df["ai_money"] / df["total_market_money"]

ai_share_peak = df.loc[df["ai_share"].idxmax()]

log_print(ai_share_peak)


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
# ② 文化強度最大世代
# ==============================
log_print("\n===== ② 文化強度最大世代 =====")
max_ideo_row = df.loc[df["avg_ideology_strength"].idxmax()]
log_print(max_ideo_row)
picked_rows.append(max_ideo_row)

# ==============================
# ③ 文化強度最小世代（思想混乱期）
# ==============================
log_print("\n===== ③ 文化強度最小世代 =====")
min_ideo_row = df.loc[df["avg_ideology_strength"].idxmin()]
log_print(min_ideo_row)
picked_rows.append(min_ideo_row)

# ==============================
# ④ 覇権戦略革命
# ==============================
log_print("\n===== ④ 覇権戦略革命 =====")

prev_top = None
for _, row in df.iterrows():
    money = {
        "speed": row["money_speed"],
        "stamina": row["money_stamina"],
        "balance": row["money_balance"],
    }
    top = max(money, key=money.get)

    if prev_top is not None and top != prev_top:
        log_print(f"世代 {int(row['gen'])} → 戦略革命: {top}")
        picked_rows.append(row)

    prev_top = top

# ==============================
# ⑤ 思想革命（資金ベース）
# ==============================
log_print("\n===== ⑤ 思想革命（資金ベース） =====")

prev_type = None
for _, row in df.iterrows():
    money = {
        "trend": row["money_trend"],
        "anti": row["money_anti"],
        "spin": row["money_spin"],
    }
    top = max(money, key=money.get)

    if prev_type is not None and top != prev_type:
        log_print(f"世代 {int(row['gen'])} → 思想革命: {top}")
        picked_rows.append(row)

    prev_type = top

# ==============================
# ⑥ 文化革命（強度急変）
# ==============================
log_print("\n===== ⑥ 文化革命（強度急変） =====")

df["ideology_diff"] = df["avg_ideology_strength"].diff().abs()

revolution_threshold = 0.15  # 調整可

revolution_rows = df[df["ideology_diff"] > revolution_threshold]

for _, row in revolution_rows.iterrows():
    log_print(
        f"世代 {int(row['gen'])} → 文化強度急変 Δ={row['ideology_diff']:.3f}"
    )
    picked_rows.append(row)

# ==============================
# ⑦ 文化フェーズ判定
# ==============================
log_print("\n===== ⑦ 文化フェーズ =====")

for _, row in df.iterrows():

    counts = [
        row["count_trend"],
        row["count_anti"],
        row["count_spin"]
    ]

    active_types = sum(1 for c in counts if c > 0)

    if active_types == 1:
        log_print(f"世代 {int(row['gen'])} → 文化統一時代")
        picked_rows.append(row)

    elif active_types == 3:
        log_print(f"世代 {int(row['gen'])} → 多極文化時代")
        picked_rows.append(row)

# ==============================
# ⑧ 思想別強度逆転
# ==============================
log_print("\n===== ⑧ 思想強度逆転 =====")

prev_strongest = None

for _, row in df.iterrows():
    strength = {
        "trend": row["strength_trend"],
        "anti": row["strength_anti"],
        "spin": row["strength_spin"],
    }

    strongest = max(strength, key=strength.get)

    if prev_strongest is not None and strongest != prev_strongest:
        log_print(f"世代 {int(row['gen'])} → 強度覇権交代: {strongest}")
        picked_rows.append(row)

    prev_strongest = strongest


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