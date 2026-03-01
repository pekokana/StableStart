# StableStart

StableStart は、競馬を題材にした **進化型エコシステムシミュレーター** です。

検討に関する情報は `/docs/SUMMARY.md`の目次を参考に参照してください。

本プロジェクトでは以下を探究します：

* 進化ダイナミクス
* 環境適応
* 競争経済システム
* AIによる育成戦略
* 将来的な Godot への統合

```
StableStart is an evolutionary horse-racing ecosystem simulator.

This project explores:

* Evolutionary dynamics
* Environmental adaptation
* Competitive economic systems
* AI-driven training strategies
* Future integration into a Godot-based game
```


# プロジェクトの目的(Project Vision)

StableStart は、次のような動的な競馬世界を構築することを目指します。

* 血統が環境圧により進化する
* 経済競争が自然淘汰を加速させる
* 戦略が台頭し、やがて崩壊する
* 覇権血統が誕生し、滅びる
* 環境ショックが世界構造を変える

最終目標は、この検証済みシミュレーションコアを Godot エンジンへ統合し、ゲームとして実装することです。


```
StableStart aims to simulate a dynamic horse-racing world where:

* Bloodlines evolve under environmental pressure
* Economic competition drives natural selection
* Strategies rise and collapse
* Dominant dynasties emerge and fall
* Shock events reshape the ecosystem

The long-term goal is to integrate this validated simulation core into a Godot game engine environment.

```

---

# 現在のフェーズ(Current Phase)

現在は「世界検証フェーズ」として、以下を実装・検証しています。

* 10エージェント競争経済モデル
* 1000世代の長期安定性検証
* 距離トレンドの周期変動＋ショックイベント
* 怪物的突然変異イベント
* 総賞金固定の分配経済
* 破産による市場退場

この段階では、ゲーム実装ではなく、
**長期的に崩壊しない人工進化世界の構築** を目的としています。

```
We are currently implementing:

* 10-agent competitive economic model
* 1000-generation stability testing
* Environmental distance cycles + shock events
* Monster mutation events
* Fixed total prize distribution
* Bankruptcy and market exit

This phase focuses on validating long-term ecosystem stability before engine integration.
```

# シミュレーション設計(Simulation Design)

## 進化モデル(Evolution Model)

* 遺伝子：Speed / Stamina
* 通常突然変異＋低確率の怪物変異
* 戦略別繁殖選択

```
* Speed / Stamina genes
* Mutation + rare monster events
* Strategy-based breeding
```


## 経済モデル(Economy Model)

* 総賞金固定の分配制
* 能力に比例する維持費
* 破産退場
* 資本の集中と淘汰

```
* Fixed total prize pool
* Maintenance costs per horse
* Bankruptcy elimination
* Competitive capital accumulation
```

## 環境モデル(Environment)

* 距離トレンドの周期変動
* ランダムショックイベント

```
* Cyclic distance trend
* Random shock events
```

# 今後のロードマップ(Roadmap)

* [ ] 1000世代安定性の統計検証
* [ ] 血統クラスタ分析
* [ ] ニューラルネット調教師の導入
* [ ] 多地域世界シミュレーション
* [ ] Godot への統合

```
* [ ] 1000 generation stability validation
* [ ] Bloodline cluster analysis
* [ ] Neural network trainer agents
* [ ] Multi-region world simulation
* [ ] Godot engine integration
```

# 今後の展望(Future Direction)

StableStart は単なるゲーム試作ではありません。

**シンプルなルールからドラマを生み出す人工進化実験場** です。

進化・経済・環境が相互作用することで、
予測不能な物語が自然発生する世界の構築を目指します。

```
StableStart is not just a game prototype.

It is an experimental artificial evolution laboratory designed to create emergent drama from simple rules.
```