#!/data/data/com.termux/files/usr/bin/bash
# Load .env dan generate config.js
set -a
source .env
set +a

cat > config.js << JS
window.FIREBASE_CONFIG = {
  apiKey: "${FIREBASE_API_KEY}",
  authDomain: "${FIREBASE_AUTH_DOMAIN}",
  projectId: "${FIREBASE_PROJECT_ID}",
  storageBucket: "${FIREBASE_STORAGE_BUCKET}",
  messagingSenderId: "${FIREBASE_MESSAGING_SENDER_ID}",
  appId: "${FIREBASE_APP_ID}"
};
JS

echo "✅ config.js dibuat dari .env"
