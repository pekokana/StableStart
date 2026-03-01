
# 📁 ディレクトリ構成問題（重要）

今の状況：

* ローカルはGodotプロジェクト
* Pythonで世界検証コードを書いている

このまま混在させるのは

👉 ❌ 将来ほぼ確実に後悔します

---

# ✅ 最適な構成

GitHub上はこうするのが理想：

```
StableStart/
│
├── simulation/        ← 研究用Python
│   ├── core.py
│   ├── economy.py
│   ├── evolution.py
│   ├── experiments/
│   └── requirements.txt
│
├── godot/             ← Godotプロジェクト
│   ├── project.godot
│   ├── scenes/
│   └── scripts/
│
├── docs/
│
└── README.md
```

---

# 🎯 なぜ分けるべき？

理由：

### 1️⃣ 役割が違う

* simulation = 数理エンジン研究所
* godot = 表示とUI

---

### 2️⃣ Godotはバイナリファイルが多い

Git管理が汚れる

---

### 3️⃣ 将来こうなる

* Python検証が巨大化
* 機械学習導入
* 可視化Notebook追加

混在していると地獄になります。

---

# 💡 ベスト運用方法

## ✅ 同一GitHubリポジトリでOK

でもフォルダ分離する。

## ❌ 別リポジトリに分ける必要はない（今は）

---

# 🧠 さらにプロっぽくするなら

```
simulation/
	src/
	experiments/
	notebooks/
```

まで分けても良い。

---

# 🚨 今やってはいけないこと

* Godot直下にPython置く
* project.godotと同じ階層に検証コード
* 実験コードと本番コード混在

---

# 🎯 あなたの今のフェーズは？

完全に：

> 🎓 研究フェーズ

Godotはまだ不要。

むしろ

👉 **simulationフォルダを主役にすべき**

---

# 🔥 次のアクション提案

1. GitHub上で `simulation/` ディレクトリ作成
2. 今のコードをそこへ移動
3. requirements.txt 追加
4. README更新

---

結果が出たら教えてください。

その次は：

* 📊 可視化追加
* 🧬 血統クラスタ分析強化
* 🤖 NN調教師導入

StableStart、もう研究プロジェクトです。

次の結果、楽しみにしてます。
