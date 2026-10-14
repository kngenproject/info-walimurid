#!/data/data/com.termux/files/usr/bin/bash
# Generate config.js dari .env
# Jalankan: bash generate-config.sh

set -e
cd "$(dirname "$0")"

if [ ! -f .env ]; then
  echo "❌ File .env tidak ditemukan."
  echo "   Salin dulu: cp .env.example .env"
  echo "   Lalu isi kredensial Firebase Anda."
  exit 1
fi

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
