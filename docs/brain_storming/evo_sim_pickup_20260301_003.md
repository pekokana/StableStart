```
２回シミュレートした結果を貼り付けます。

## １回目
‘‘‘PS D:\dev\StableStart\simulation> uv run .\pickup_evolution_test4.py
===== ① 最終世代 =====
gen              9.990000e+02
agents           2.000000e+00
avg_speed        9.721984e-01
avg_stamina      9.630328e-01
trend            2.290760e+03
speed_ratio      0.000000e+00
stamina_ratio    0.000000e+00
balance_ratio    1.000000e+00
money_speed      0.000000e+00
money_stamina    0.000000e+00
money_balance    3.765977e+08
Name: 999, dtype: float64

===== ② エージェント数が最小の世代 =====
gen              2.900000e+01
agents           2.000000e+00
avg_speed        9.601172e-01
avg_stamina      9.784980e-01
trend            1.744611e+03
speed_ratio      0.000000e+00
stamina_ratio    0.000000e+00
balance_ratio    1.000000e+00
money_speed      0.000000e+00
money_stamina    4.447182e+06
money_balance    0.000000e+00
Name: 29, dtype: float64

===== ③ トレンド最大（長距離ピーク） =====
gen              6.900000e+01
agents           2.000000e+00
avg_speed        9.570861e-01
avg_stamina      9.772029e-01
trend            2.400000e+03
speed_ratio      0.000000e+00
stamina_ratio    5.000000e-02
balance_ratio    9.500000e-01
money_speed      0.000000e+00
money_stamina    1.979887e+07
money_balance    0.000000e+00
Name: 69, dtype: float64

===== ④ トレンド最小（短距離ピーク） =====
gen              7.100000e+01
agents           2.000000e+00
avg_speed        9.792858e-01
avg_stamina      9.642189e-01
trend            1.200000e+03
speed_ratio      0.000000e+00
stamina_ratio    0.000000e+00
balance_ratio    1.000000e+00
money_speed      0.000000e+00
money_stamina    6.398261e+06
money_balance    1.416893e+07
Name: 71, dtype: float64

===== ⑤ 平均能力最大世代 =====
gen              1.410000e+02
agents           2.000000e+00
avg_speed        9.915406e-01
avg_stamina      9.808834e-01
trend            1.340370e+03
speed_ratio      5.000000e-02
stamina_ratio    0.000000e+00
balance_ratio    9.500000e-01
money_speed      0.000000e+00
money_stamina    4.741622e+07
money_balance    0.000000e+00
avg_total        1.972424e+00
Name: 141, dtype: float64

===== ⑥ 覇権戦略が変わった世代 =====
世代: 17 → 覇権: speed
世代: 18 → 覇権: stamina
世代: 54 → 覇権: balance
世代: 59 → 覇権: stamina
世代: 71 → 覇権: balance
世代: 84 → 覇権: speed
世代: 105 → 覇権: stamina
世代: 127 → 覇権: balance
世代: 135 → 覇権: stamina
世代: 179 → 覇権: balance
世代: 196 → 覇権: stamina
世代: 231 → 覇権: balance
世代: 236 → 覇権: speed
世代: 251 → 覇権: balance
世代: 281 → 覇権: stamina
世代: 299 → 覇権: speed
世代: 342 → 覇権: balance
世代: 364 → 覇権: stamina
世代: 396 → 覇権: balance
世代: 401 → 覇権: stamina
世代: 404 → 覇権: balance
世代: 411 → 覇権: speed
世代: 432 → 覇権: balance
世代: 494 → 覇権: speed
世代: 558 → 覇権: stamina
世代: 561 → 覇権: balance
世代: 564 → 覇権: speed
世代: 567 → 覇権: stamina
世代: 578 → 覇権: balance
世代: 606 → 覇権: speed
世代: 611 → 覇権: balance
世代: 662 → 覇権: stamina
世代: 682 → 覇権: balance
世代: 689 → 覇権: speed
世代: 710 → 覇権: balance
世代: 727 → 覇権: stamina
世代: 746 → 覇権: balance
世代: 783 → 覇権: stamina
世代: 785 → 覇権: balance
世代: 795 → 覇権: speed
世代: 812 → 覇権: balance
世代: 819 → 覇権: stamina
世代: 838 → 覇権: speed
世代: 869 → 覇権: balance
世代: 785 → 覇権: balance
世代: 795 → 覇権: speed
世代: 812 → 覇権: balance
世代: 819 → 覇権: stamina
世代: 785 → 覇権: balance
世代: 795 → 覇権: speed
世代: 812 → 覇権: balance
世代: 819 → 覇権: stamina
世代: 838 → 覇権: speed
世代: 785 → 覇権: balance
世代: 795 → 覇権: speed
世代: 812 → 覇権: balance
世代: 819 → 覇権: stamina
世代: 785 → 覇権: balance
世代: 795 → 覇権: speed
世代: 812 → 覇権: balance
世代: 785 → 覇権: balance
世代: 795 → 覇権: speed
世代: 785 → 覇権: balance
世代: 795 → 覇権: speed
世代: 812 → 覇権: balance
世代: 785 → 覇権: balance
世代: 795 → 覇権: speed
世代: 785 → 覇権: balance
世代: 795 → 覇権: speed
世代: 785 → 覇権: balance
世代: 795 → 覇権: speed
世代: 785 → 覇権: balance
世代: 785 → 覇権: balance
世代: 795 → 覇権: speed
世代: 812 → 覇権: balance
世代: 819 → 覇権: stamina
世代: 838 → 覇権: speed
世代: 869 → 覇権: balance

===== ⑦ 100世代ごとのスナップショット =====
     gen  agents  avg_speed  avg_stamina        trend  speed_ratio  stamina_ratio  balance_ratio   money_speed  money_stamina  money_balance  avg_total
0      0      20   0.563275     0.575663  1785.965362         0.29          0.325          0.385  5.178094e+06   6.576412e+06   3.600920e+06   1.138938
100  100       2   0.976193     0.976400  2213.968247         0.00          0.000          1.000  2.229583e+07   0.000000e+00   9.394318e+06   1.952593
200  200       2   0.969426     0.972542  1730.499871         0.00          0.050          0.950  2.145379e+07   4.858639e+07   0.000000e+00   1.941968
300  300       2   0.963795     0.968226  1965.364203         0.00          0.100          0.900  6.988840e+07   3.851135e+07   0.000000e+00   1.932020
400  400       2   0.987795     0.969236  2202.656726         0.05          0.000          0.950  0.000000e+00   0.000000e+00   1.467831e+08   1.957031
500  500       2   0.954405     0.974926  1921.795616         0.00          0.100          0.900  1.851532e+08   0.000000e+00   0.000000e+00   1.929331
600  600       2   0.955119     0.970334  1898.295419         0.00          0.100          0.900  0.000000e+00   0.000000e+00   2.235196e+08   1.925453
700  700       2   0.968250     0.981527  1412.183641         0.00          0.050          0.950  2.618721e+08   0.000000e+00   0.000000e+00   1.949776
800  800       2   0.975399     0.977477  1214.640243         0.00          0.000          1.000  3.002607e+08   0.000000e+00   0.000000e+00   1.952876
900  900       2   0.968258     0.987508  1873.531567         0.05          0.050          0.900  0.000000e+00   0.000000e+00   3.386348e+08   1.955766

抽出ログを picked_simulation_ver4_log_20260301_225017.csv に保存しました‘‘‘

## 2回目
```===== ① 最終世代 =====
gen              9.000000e+00
agents           2.000000e+00
avg_speed        8.683371e-01
avg_stamina      9.731825e-01
trend            1.855298e+03
speed_ratio      0.000000e+00
stamina_ratio    5.000000e-01
balance_ratio    5.000000e-01
money_speed      3.955725e+06
money_stamina    0.000000e+00
money_balance    0.000000e+00
Name: 9, dtype: float64

===== ② エージェント数が最小の世代 =====
gen              5.000000e+00
agents           2.000000e+00
avg_speed        8.111738e-01
avg_stamina      8.852594e-01
trend            1.777387e+03
speed_ratio      1.000000e-01
stamina_ratio    4.000000e-01
balance_ratio    5.000000e-01
money_speed      2.381377e+06
money_stamina    0.000000e+00
money_balance    0.000000e+00
Name: 5, dtype: float64

===== ③ トレンド最大（長距離ピーク） =====
gen              9.000000e+00
agents           2.000000e+00
avg_speed        8.683371e-01
avg_stamina      9.731825e-01
trend            1.855298e+03
speed_ratio      0.000000e+00
stamina_ratio    5.000000e-01
balance_ratio    5.000000e-01
money_speed      3.955725e+06
money_stamina    0.000000e+00
money_balance    0.000000e+00
Name: 9, dtype: float64

===== ④ トレンド最小（短距離ピーク） =====
gen              5.000000e+00
agents           2.000000e+00
avg_speed        8.111738e-01
avg_stamina      8.852594e-01
trend            1.777387e+03
speed_ratio      1.000000e-01
stamina_ratio    4.000000e-01
balance_ratio    5.000000e-01
money_speed      2.381377e+06
money_stamina    0.000000e+00
money_balance    0.000000e+00
Name: 5, dtype: float64

===== ⑤ 平均能力最大世代 =====
gen              9.000000e+00
agents           2.000000e+00
avg_speed        8.683371e-01
avg_stamina      9.731825e-01
trend            1.855298e+03
speed_ratio      0.000000e+00
stamina_ratio    5.000000e-01
balance_ratio    5.000000e-01
money_speed      3.955725e+06
money_stamina    0.000000e+00
money_balance    0.000000e+00
avg_total        1.841520e+00
Name: 9, dtype: float64

===== ⑥ 覇権戦略が変わった世代 =====
世代: 3 → 覇権: speed

===== ⑦ 100世代ごとのスナップショット =====
   gen  agents  avg_speed  avg_stamina        trend  speed_ratio  stamina_ratio  balance_ratio   money_speed  money_stamina  money_balance  avg_total
0    0      20   0.523101     0.593905  1805.353557        0.105           0.43          0.465  3.725137e+06   9.471289e+06   2.161329e+06   1.117006

抽出ログを picked_simulation_ver4_log_20260301_225345.csv に保存しました```

@@@@@
素晴らしい。
これはもう「挙動の癖」がはっきり見えています。

結論から言います。

---

# 🔎 1回目のシミュレーション解析

### ✅ 最終状態

* エージェント数：**2**
* 戦略比率：**100% balance**
* 資金：**balanceが独占（3.7億）**

### ✅ 重要な現象

1. **ほぼ全期間でエージェント2体固定**
2. 覇権は頻繁に交代
3. しかし最終的に balance 一強
4. 能力はほぼ上限張り付き（~0.97）

---

## 🧠 これは何が起きているか？

### ① 早期に大量淘汰が発生

100世代時点で agents=2
→ 競争が事実上「デュオポリー」状態

### ② 能力が飽和

avg_total ≈ 1.95
ほぼ天井に張り付き

進化圧がほぼ停止

### ③ 経済が循環している

覇権はスイングしているが
最終的に balance に吸収

これは

> 🧬 「進化循環モデル」になっている

かなり良い挙動です。

---

# 🔎 ただし重大なバグが見えています

覇権ログにこれがあります：

```
世代: 785 → 覇権: balance
世代: 795 → 覇権: speed
世代: 812 → 覇権: balance
世代: 819 → 覇権: stamina
世代: 785 → 覇権: balance
...
```

同じ世代が何度も出ています。

これは：

```python
picked_rows.append(row)
```

を snapshot でも追加しているため
重複ループしている可能性大です。

---

# 🔎 2回目シミュレーション

こちらは完全に別の問題。

### ❗ gen=9 で終了している

つまり

> 💥 世界が崩壊している

---

## 状況整理

* 5世代で最小エージェント到達
* 9世代で終了
* 覇権交代1回のみ

これは

### 💀 経済が即座に単一戦略にロック

している状態。

---

# 🎯 2回の違いの意味

|      | 1回目    | 2回目 |
| ---- | ------ | --- |
| 生存期間 | 1000世代 | 9世代 |
| 戦略循環 | あり     | なし  |
| 経済構造 | 振動型    | 即崩壊 |
| 進化圧  | 継続     | 急停止 |

---

# 🧠 重要な洞察

今のモデルは

> 初期乱数によって
> 「循環世界」か「崩壊世界」かに分岐する

つまり：

### 🌍 分岐型進化経済モデル

になっています。

これは研究としてかなり面白い。

---

# ⚠ 今最大の問題

## 🔴 エージェントが2体まで減りすぎる

10エージェントで始めたのに
2体固定は

> 競争経済としては不十分

---

# 🔧 次にやるべきこと

### ① 最低人口維持（例：5体以下にならない）

```
min_agents = 5
```

### ② 破産しても完全消滅させない

* 再参入
* 低資金で復活
* クローン生成

---

# 🔥 一番重要な問い

あなたの世界は

* 🧬 「淘汰重視モデル」か
* 🏛 「経済循環モデル」か

どちらを目指しますか？

今は淘汰圧が強すぎます。

---

# 🎯 個人的提案

B：ドラマ重視
A：経済リアル寄り

なら

### ✔ 最低人口5維持

### ✔ 資金再分配微量導入

### ✔ 破産即消滅をやめる

これで

* 崩壊せず
* 循環し
* 覇権が揺れる世界

になります。

---

ここからが本当に面白いフェーズです。

次は：

* 「最低人口制限を入れたバージョン」
* それとも
* 「あえて崩壊確率を測る実験」

どちらに進みますか？
