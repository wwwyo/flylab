# loom-escape

視覚の looming 検出（LC4 / LPLC2）→ 逃避指令ニューロン（DNp01 = giant fiber）の回路を、MaleCNS 全グラフ（166,700 ニューロン / 25.6M edges）そのままの配線で通す最小実験。

## 何を確かめるか

コネクトーム由来の LIF モデルで「感覚 → 下行ニューロン」まで信号が届くか、届くなら生物として正しい側（同側性）に届くか。

- 静息時: descending neuron が ~1 Hz で静かに保たれるか（これが保てないと反応が読めない。tonic/gain の calibration が効いているかの確認）
- loom 注入: 左目の LC4+LPLC2 に電流を入れた fly 0 は左の DNp01 が、右目に入れた fly 1 は右の DNp01 が発火し、反対側は沈黙するか（ipsilateral 伝播）
- どの descending cell type が下流で発火したか（逃避系以外も巻き込むか）

## 実行

```bash
uv run loom-escape/main.py
```

初回は `~/fly-data` に脳データ（~260MB）をダウンロードする。

## 前提・限界

- 重みは解剖データ由来の推定値（シナプス接触数比例 + 予測伝達物質の符号）。実測値ではない
- 全ニューロン同一 LIF パラメータ、ギャップ結合・神経修飾なし
- 注入は細胞タイプへの一様電流。実際の網膜入力パターンの再現ではない（`FeatureDetectors`/`Eyes` を使うと網膜→lobula 経路を通せる）
- この PoC が通ることは「配線が機能的か」の十分条件ではなく、信号が届くことの確認に留まる
