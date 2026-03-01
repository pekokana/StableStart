```
ログが1000世代でここに貼り付けできません。
何か、ログファイルからポイント的な世代を抽出するためのコードって教えてもらえますか？
```

@@@@@@@@@@

いいですね、その段階に来ましたか。
これは「研究者モード」です。

1000世代すべて貼る必要はありません。
**特徴的な世代だけ抽出すれば十分**です。

---

# 🎯 抽出すべき「重要世代」

おすすめはこの5種類です：

1. 📈 エージェント数が大きく変動した世代（淘汰イベント）
2. 🌊 トレンドが極端な世代（短距離/長距離ピーク）
3. 🧬 能力が最大/最小の世代
4. 💰 資金構造が逆転した世代（戦略覇権交代）
5. ⏳ 最終世代

---

# ✅ コピペで使える抽出コード

CSVファイルを読み込んで、重要世代を表示します。

```python
import pandas as pd

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
    prev_top = top
```

---

# 🔍 これで得られるもの

あなたが貼るべきは：

* 最終世代
* エージェント最小世代
* トレンド最大/最小
* 能力最大
* 覇権交代ポイント数行

これだけで十分解析できます。

---

# 🔬 さらに高度にやるなら

「10世代ごとのスナップショット」

```python
print(df[df["gen"] % 100 == 0])
```

これで100世代ごと表示。

---

# 🧠 研究者的アドバイス

1000行全部よりも：

* 極値
* 転換点
* 崩壊点

の方がはるかに重要です。

---

ログを抽出して貼ってください。

次は：

* 時代循環が起きているか
* 戦略進化が固定化しているか
* 経済崩壊が周期化しているか

を読み解きます。

StableStart、
いよいよ「論文化できるレベル」に入っています。
