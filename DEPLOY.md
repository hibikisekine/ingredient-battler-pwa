# 🚀 成分表示バトラー - デプロイ手順

## 📋 デプロイ方法

### 1. Vercel（推奨）

**手順:**
1. [Vercel](https://vercel.com)にアカウント登録
2. GitHubリポジトリを接続
3. 自動デプロイが開始

**設定:**
- Framework Preset: Other
- Build Command: `pip install -r requirements.txt`
- Output Directory: `public`
- Install Command: `pip install -r requirements.txt`

### 2. Netlify

**手順:**
1. [Netlify](https://netlify.com)にアカウント登録
2. GitHubリポジトリを接続
3. ビルド設定:
   - Build command: `pip install -r requirements.txt`
   - Publish directory: `public`

### 3. Firebase Hosting

**手順:**
1. Firebase CLIをインストール: `npm install -g firebase-tools`
2. ログイン: `firebase login`
3. プロジェクト初期化: `firebase init hosting`
4. デプロイ: `firebase deploy`

## 🔧 環境変数設定

### 本番環境用
```bash
FLASK_ENV=production
FLASK_DEBUG=0
```

### 開発環境用
```bash
FLASK_ENV=development
FLASK_DEBUG=1
```

## 📱 PWA機能確認

### インストール可能かチェック
```javascript
// ブラウザコンソールで実行
if ('serviceWorker' in navigator) {
    console.log('Service Worker対応');
}
if ('BeforeInstallPromptEvent' in window) {
    console.log('インストール可能');
}
```

### マニフェスト確認
```bash
curl https://your-domain.com/manifest.json
```

## 🎯 パフォーマンス最適化

### 1. 画像最適化
- WebP形式への変換
- レスポンシブ画像
- 遅延読み込み

### 2. キャッシュ戦略
- Service Worker キャッシュ
- CDN利用
- ブラウザキャッシュ

### 3. コード分割
- JavaScript の分割
- CSS の最適化
- 不要なライブラリの削除

## 📊 監視・分析

### Google Analytics
```html
<!-- トラッキングコード -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### エラー監視
- Sentry
- LogRocket
- Bugsnag

## 🔒 セキュリティ

### HTTPS強制
```javascript
// Service WorkerでHTTPS強制
if (location.protocol !== 'https:' && location.hostname !== 'localhost') {
    location.replace(`https:${location.href.substring(location.protocol.length)}`);
}
```

### CSP設定
```html
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://unpkg.com; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com;">
```

## 📈 スケーリング

### 1. データベース
- SQLite → PostgreSQL
- クラウドデータベース利用

### 2. キャッシュ
- Redis導入
- CDN利用

### 3. 負荷分散
- ロードバランサー
- マイクロサービス化

## 🚨 トラブルシューティング

### よくある問題

**1. Service Workerが登録されない**
```javascript
// デバッグ用
navigator.serviceWorker.register('/static/sw.js')
    .then(registration => console.log('SW registered'))
    .catch(error => console.log('SW registration failed:', error));
```

**2. マニフェストが読み込まれない**
- ファイルパス確認
- MIMEタイプ確認
- HTTPS確認

**3. インストールボタンが表示されない**
- HTTPS必須
- マニフェスト必須
- Service Worker必須

## 📞 サポート

問題が発生した場合は以下を確認:
1. ブラウザの開発者ツール
2. ネットワークタブ
3. コンソールエラー
4. Service Worker タブ

---

**成分表示バトラー** - 栄養成分でバトルを楽しもう！ 🥗⚔️ 