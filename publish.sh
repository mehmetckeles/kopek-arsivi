#!/usr/bin/env bash
# Depodaki değişiklikleri yayımlar.
# Kullanım: ./publish.sh "commit mesajı"
set -e
cd "$(dirname "$0")"

git config user.email "cihatk@gmail.com"
git config user.name  "Kopek Arsivi Bot"

git add -A
if git diff --cached --quiet; then
  echo "DEGISIKLIK_YOK"
  exit 0
fi

git commit -q -m "${1:-Yeni yazı}"

# Bu arada başka bir çalışma gönderim yapmış olabilir; önce birleştir.
git pull -q --rebase origin main || { echo "BIRLESTIRME_HATASI"; exit 1; }
git push -q origin main
echo "YAYIMLANDI"
