# 🚀 GitHubリポジトリ作成手順

## 1. GitHubでリポジトリ作成

1. [GitHub](https://github.com)にアクセス
2. 右上の「+」ボタン → 「New repository」
3. リポジトリ名: `ingredient-battler-pwa`
4. 説明: `栄養成分でキャラクターを生成してバトルするPWAアプリ`
5. Public を選択
6. 「Create repository」をクリック

## 2. ローカルリポジトリをプッシュ

```bash
# リモートリポジトリを追加
git remote add origin https://github.com/YOUR_USERNAME/ingredient-battler-pwa.git

# プッシュ
git branch -M main
git push -u origin main
```

## 3. Vercelでデプロイ

1. [Vercel](https://vercel.com)にアクセス
2. GitHubアカウントでログイン
3. 「New Project」をクリック
4. `ingredient-battler-pwa`リポジトリを選択
5. 設定:
   - Framework Preset: Other
   - Build Command: `pip install -r requirements.txt`
   - Output Directory: `public`
   - Install Command: `pip install -r requirements.txt`
6. 「Deploy」をクリック

## 4. カスタムドメイン設定（オプション）

1. Vercelプロジェクト設定
2. 「Domains」タブ
3. カスタムドメインを追加

## 5. 環境変数設定

Vercelプロジェクト設定で以下を追加:
- `FLASK_ENV=production`
- `FLASK_DEBUG=0`

---

**成分表示バトラー** - 栄養成分でバトルを楽しもう！ 🥗⚔️ 