# flylab

ハエ（ショウジョウバエ）のコネクトーム由来シミュレーションを触る playground。

試しているもの: MaleCNS v1.0（166,700 ニューロン / 25.6M edges）を leaky integrate-and-fire で回す `flybrain` パッケージ。解剖推定の重みだけで「感覚入力 → 下行ニューロン → 行動」まで信号が届くかを確かめ、届く回路がどこまで機能的に使えるかが分かれば採否（深掘りするか）を決められる。

## ディレクトリ構造

PoC ごとにコードと docs を同名の dir で切る。

```
flylab/
├── <poc>/           PoC ごとのコード（uv run <poc>/main.py で実行）
└── docs/<poc>/      その PoC で何を作り何を確かめるか
```

## セットアップ

ツールは mise で管理している。

```bash
mise install          # python 3.13.15 / uv 0.12.15
uv sync               # 依存を .venv にインストール
uv run <poc>/main.py  # PoC を実行
```

脳データは初回実行時に `~/fly-data` へ ~260MB ダウンロードされる（`FLY_DATA` で変更可）。データ・生成物は repo に入れない（public repo のため、ローカルのデータは env で path を受けて読む）。

## 技術スタック

- Python 3.13 + uv
- [flybrain](https://github.com/alextitonis/fly.ai) — MaleCNS 全グラフの LIF シミュレーション（CPU は numba。`device="cuda"` は NVIDIA 専用で Mac では使えない）
- 素のモデルの限界: 重みは接触数比例の推定値、全ニューロン同一 LIF、ギャップ結合・神経修飾なし
