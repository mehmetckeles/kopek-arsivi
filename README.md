# Tarihten Köpekler

Köpek ve insanlık tarihi üzerine Türkçe yazılar.

Yayında: https://mehmetckeles.github.io/kopek-arsivi/

## Yapı

| Dosya | Açıklama |
|---|---|
| `index.html` | Sitenin tamamı. Tek dosya, bağımlılık yok. |
| `articles.json` | Yazılar. Her sabah otomatik güncellenir. |
| `add_article.py` | Bir markdown yazısını `articles.json`'a ekler. |
| `publish.sh` | Değişiklikleri işleyip gönderir. |
| `build.py` | Markdown klasöründen `articles.json` üretir (toplu kurulum için). |
| `.nojekyll` | GitHub Pages'in Jekyll işlemesini atlaması için. |
| `netlify.toml` | Netlify ayarları (yedek yayın kanalı). |

Bu depoya yapılan her gönderim otomatik yayımlanır.
Yazılar Cowork'te zamanlanmış bir görevle üretilir ve buraya gönderilir.
