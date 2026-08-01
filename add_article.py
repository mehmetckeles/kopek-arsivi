#!/usr/bin/env python3
"""
Tek bir markdown makalesini articles.json'a ekler.

Kullanım:
    python3 add_article.py yeni.md [ISO-tarih]

Tarih verilmezse şu an kullanılır. Aynı başlık zaten varsa hiçbir şey yapmaz
(çıkış kodu 0, "zaten var" mesajı) — görev iki kez çalışırsa kopya oluşmaz.
"""
import json, os, re, sys, unicodedata
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
JSON = os.path.join(HERE, 'articles.json')

TR = str.maketrans({
    'ç':'c','Ç':'c','ğ':'g','Ğ':'g','ı':'i','İ':'i',
    'ö':'o','Ö':'o','ş':'s','Ş':'s','ü':'u','Ü':'u',
    'â':'a','Â':'a','î':'i','Î':'i','û':'u','Û':'u',
})

def slugify(s, limit=70):
    s = s.translate(TR).lower()
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    if len(s) <= limit:
        return s
    cut = s[:limit]
    if s[limit] != '-':
        cut = cut.rsplit('-', 1)[0]
    return cut.strip('-')

TAG_RE = re.compile(r'^\s*\**Etiket önerileri:\**\s*(.+)$', re.M | re.I)

def parse(md):
    # Drive'ın kaçışlı biçimini temizle (\# , \*\* , \--- gibi)
    md = re.sub(r'\\([#*\-_`>\[\]()~+.!])', r'\1', md)
    md = re.sub(r'[ \t]+$', '', md, flags=re.M)

    tags = []
    m = TAG_RE.search(md)
    if m:
        tags = [t.strip().replace('*', '').lower()
                for t in re.split(r'[,·]', m.group(1)) if t.strip()]
        md = md[:m.start()]
    md = re.sub(r'\n-{3,}\s*$', '', md.rstrip()).rstrip()

    t = re.search(r'^#\s+(.+)$', md, re.M)
    title = t.group(1).strip() if t else None
    return title, md.strip(), tags

def main():
    if len(sys.argv) < 2:
        sys.exit('kullanım: add_article.py <dosya.md> [ISO-tarih]')

    raw = open(sys.argv[1], encoding='utf-8').read()
    date = sys.argv[2] if len(sys.argv) > 2 else datetime.now(timezone.utc).isoformat()

    title, body, tags = parse(raw)
    if not title:
        sys.exit('HATA: başlık (# ...) bulunamadı')
    if len(body) < 400:
        sys.exit('HATA: gövde çok kısa (%d karakter)' % len(body))

    articles = json.load(open(JSON, encoding='utf-8')) if os.path.exists(JSON) else []

    if any(a['title'].strip() == title for a in articles):
        print('zaten var, atlandı:', title)
        return

    base = slugify(title)
    taken = {a['slug'] for a in articles}
    slug, n = base, 2
    while slug in taken:
        slug = f'{base}-{n}'; n += 1

    articles.append({'slug': slug, 'title': title, 'date': date,
                     'tags': tags, 'content': body})
    articles.sort(key=lambda a: a['date'], reverse=True)

    with open(JSON, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=1)

    print(f'eklendi: {title}')
    print(f'  slug   : {slug}')
    print(f'  etiket : {", ".join(tags) if tags else "(yok)"}')
    print(f'  toplam : {len(articles)} makale')

if __name__ == '__main__':
    main()
