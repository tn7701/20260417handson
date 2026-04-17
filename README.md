# Pomodoro Timer Web App

Flask + HTML/CSS/JavaScript で作成したポモドーロタイマーです。`1.pomodoro/` 配下にアプリ本体があります。

## 起動

```bash
python3 app.py
```

ブラウザで `http://127.0.0.1:5000` を開くと、タイマー画面が表示されます。

## テスト

```bash
python3 -m pytest -q
```

## 主な構成

- `1.pomodoro/pomodoro/` : Flask アプリ、API、サービス、モデル
- `1.pomodoro/templates/` : HTML テンプレート
- `1.pomodoro/static/` : CSS と JavaScript
- `tests/` : 単体テスト
