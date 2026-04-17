# Pomodoro Timer

Flask + HTML/CSS/JavaScript で構成したポモドーロタイマーです。

## 起動

```bash
python3 1.pomodoro/app.py
```

ブラウザで `http://127.0.0.1:5000` を開くと、タイマー画面が表示されます。

## テスト

```bash
python3 -m pytest -q
```

## 構成

- `1.pomodoro/pomodoro/` : Flask アプリ本体、API、サービス層、モデル
- `1.pomodoro/templates/` : HTML テンプレート
- `1.pomodoro/static/` : CSS と JavaScript
- `tests/` : API とタイマーサービスの単体テスト

