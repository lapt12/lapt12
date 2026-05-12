<div align="center">

<!-- Animated Header -->
<img src="./banner.svg" width="100%"/>

<!-- Typing Animation -->
<a href="https://git.io/typing-svg">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&amp;weight=600&amp;size=22&amp;pause=1000&amp;color=A78BFA&amp;center=true&amp;vCenter=true&amp;random=false&amp;width=600&amp;lines=Discord+Bot+Developer;Python+%26+Java+Engineer;Game+Developer" alt="Typing SVG" />
</a>
<br/>
</div>

## About Me
<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-Apt(lapt12)-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/lapt12)
[![Discord](https://img.shields.io/badge/Discord-Bot%20Developer-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com)

</div>
<p align="center">
aptです、DiscordBotとゲーム開発、機械学習が好きなアマチュアエンジニアです。  
<Br>
非同期処理・UIコンポーネント設計・AI設計に特に力を入れて遊んでいます。
<Br>
現在はmp3をピアノの音で再現する機械学習アプリを作成しています。
<Br>
今後は2.5DGameの派生作品も作っていく予定です。
</p>

## Tech Stack

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Java](https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white)
![Rust](https://img.shields.io/badge/Rust-f05b50?style=for-the-badge&logo=rust&logoColor=white)
<Br>
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Discord](https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)
![FFmpeg](https://img.shields.io/badge/FFmpeg-007808?style=for-the-badge&logo=ffmpeg&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)

</div>

## Projects

### < Myrtle — Java 2.5D R.E.P.O >
<div>
<img src="https://img.shields.io/badge/Java-Swing-ED8B00?style=flat-square&amp;logo=openjdk&amp;logoColor=white"/>
<img src="https://img.shields.io/badge/Genre-Dungeon%20Crawler-8B5CF6?style=flat-square"/>
<img src="https://img.shields.io/badge/Status-Complete-22c55e?style=flat-square"/>
</div>
<Br>

> Javaとswingで構築した2,5Dダンジョン探索ゲームです、レイキャスト方式によるコンソール風レンダリング、スタミナ管理、セーブスロット機能（5スロット）を実装しました。

**主な実装内容**
- `ConsoleRenderer.java` — レイキャストによる3Dビュー描画
- `GameMap.java` — タイル制マップ・当たり判定・敵配置
- `Player.java` — 移動・ジャンプ・スタミナ・ダメージ処理
- `UserData.java` — JSONベースのセーブ/ロード機構

```
📦 Myrtle
├── Main.java              # エントリーポイント
├── GameFrame.java         # ウィンドウ管理・セーブスロット選択
├── GamePanel.java         # ゲームループ・入力処理
├── ConsoleRenderer.java   # レイキャスト描画エンジン
├── Player.java            # プレイヤーの物理・状態管理
├── GameMap.java           # マップデータ・衝突判定
├── Enemy.java             # 敵AI
└── UserData.java          # セーブデータ管理
```

---

### < Splatoon-bot — スプラトゥーン専用 Discord Bot >
<div>
<img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&amp;logo=python&amp;logoColor=white"/>
<img src="https://img.shields.io/badge/discord.py-2.6.x-5865F2?style=flat-square&amp;logo=discord&amp;logoColor=white"/>
<img src="https://img.shields.io/badge/Type-Guild%20Install-60b13c?style=flat-square"/>
<img src="https://img.shields.io/badge/Status-Inactive-ff1100?style=flat-square"/>
</div>
<div>
<img src="https://img.shields.io/badge/DB-SQLite%20%2B%20aiosqlite-003B57?style=flat-square&amp;logo=sqlite&amp;logoColor=white"/>
<img src="https://img.shields.io/badge/AI-Gemini%20API-4285F4?style=flat-square&amp;logo=google&amp;logoColor=white"/>
</div>
<Br>

> スプラトゥーンのDiscordサーバー向け運営支援Botです、募集ボード・ステージ自動更新・メンバー管理・セキュリティ・AI通報解析を行いサーバー運営を支援を実現しました。

| 機能 | 概要 |
|------|------|
|  募集ボード | ナワバリ/ガチマ/Xマッチ/サモランの募集ボード自動生成と参加管理 |
|  データボード | Splatoon APIで2時間毎にステージボードメッセージの情報を自動更新 |
|  セキュリティ | トークン漏洩検知・自動削除・24時間タイムアウト |
|  報告システム | Gemini APIによる通報内容の自動解析・スコアリング |
|  音楽再生 | yt-dlp + FFmpegによる低遅延VCストリーミング |
|  緊急停止 | DB保存・ログ出力後の安全なBot停止システム |

---

### < 紅霞 (Kouka) — モダンUI Discord Bot >
<div>
<img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&amp;logo=python&amp;logoColor=white"/>
<img src="https://img.shields.io/badge/discord.py-2.6.x-5865F2?style=flat-square&amp;logo=discord&amp;logoColor=white"/>
<img src="https://img.shields.io/badge/Type-Guild%20Install-60b13c?style=flat-square"/>
<img src="https://img.shields.io/badge/Status-Active-22c55e?style=flat-square"/>
</div>
<div>
<img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&amp;logo=fastapi&amp;logoColor=white"/>
<img src="https://img.shields.io/badge/yt--dlp-FF0000?style=flat-square&amp;logo=youtube&amp;logoColor=white"/>
</div>
<Br>

> モダンな動的UIでDiscordサーバーの多様な機能を提供することを目指したBotです、音楽再生・グローバルチャット・投票システム・素数ゲームなど、多方の機能を充実させました。

**搭載機能:** 音楽再生 / グローバルチャット / チャンネル情報 / 投票システム / 語彙テスト / 素数ゲーム / YouTube展開 / ヘルプUI

**アーキテクチャ:** イベント駆動の階層設計（`events/` → `main_functions/` → `setup_funcs/`）

---

### < Aulus — 多機能 Discord Bot  >
<div>
<img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&amp;logo=python&amp;logoColor=white"/>
<img src="https://img.shields.io/badge/discord.py-2.x-5865F2?style=flat-square&amp;logo=discord&amp;logoColor=white"/>
<img src="https://img.shields.io/badge/Type-Guild%20Install-60b13c?style=flat-square"/>
  <img src="https://img.shields.io/badge/Status-Inactive-ff1100?style=flat-square"/>
</div>
<img src="https://img.shields.io/badge/Gemini%20AI-4285F4?style=flat-square&amp;logo=google&amp;logoColor=white"/>
<Br>

> Koukaの原型となったDiscordの機能を拡張する多機能Botです、こちらも不適切な発言のAI自動判定・経済ゲーム・スパム対策・YouTube展開など幅広い機能を持たせました。

| コマンド | 説明 |
|---------|------|
| `m!gemini` | Gemini AIへの質問 |
| `m!rp` | AIによる不適切発言の判定・処罰 |
| `m!eco` | 経済/投資/カジノゲーム |
| `m!timesend` | 指定時刻への自動メッセージ送信 |
| TCS(自動検知) | 英字→日本語の自動変換システム |
| AMS(自動検知) | スパム検知・自動タイムアウト |

---

### < OPEN_TOEIC — TOEIC単語学習 Bot >
<div>
<img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&amp;logo=python&amp;logoColor=white"/>
<img src="https://img.shields.io/badge/discord.py-2.6.x-5865F2?style=flat-square&amp;logo=discord&amp;logoColor=white"/>
<img src="https://img.shields.io/badge/Type-User%20Install-7c3aed?style=flat-square"/>
<img src="https://img.shields.io/badge/Status-Stable-22c55e?style=flat-square"/>
</div>
<img src="https://img.shields.io/badge/Words-1250%E8%AA%9E-f59e0b?style=flat-square"/>
<Br>

> 1250語をQuiz1〜10に分割した4択TOEIC単語テストBotです、英→日/日→英の両モード対応させ正答率・進捗・苦手単語を自動記録し、繰り返し学習を可能にしました。

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&amp;color=0:24243e,50:302b63,100:0f0c29&amp;height=100&amp;section=footer" width="100%"/>

*by apt*

</div>
