#!/usr/bin/env python3
"""
Köpek Arşivi — site derleyici.

Girdi : *.md dosyaları (skill formatında: # Başlık ... --- **Etiket önerileri:** ...)
Çıktı : articles.json

Kullanım:
    python3 build.py <md_klasoru> <cikti.json> [tarihler.json]

tarihler.json (opsiyonel): {"01.md": "2026-07-29T10:32:32Z", ...}
Verilmezse dosyanın değiştirilme zamanı kullanılır.
"""
import json, os, re, sys, unicodedata
from datetime import datetime, timezone

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
    """markdown metni -> (baslik, govde, etiketler)"""
    m = TAG_RE.search(md)
    tags = []
    if m:
        tags = [t.strip().replace('*', '').lower()
                for t in re.split(r'[,·]', m.group(1)) if t.strip()]
        md = md[:m.start()]
    # kapanış ayıracını at
    md = re.sub(r'\n-{3,}\s*$', '', md.rstrip()).rstrip()
    t = re.search(r'^#\s+(.+)$', md, re.M)
    title = t.group(1).strip() if t else 'Başlıksız'
    return title, md.strip(), tags

def main():
    src   = sys.argv[1] if len(sys.argv) > 1 else '.'
    out   = sys.argv[2] if len(sys.argv) > 2 else 'articles.json'
    dates = {}
    if len(sys.argv) > 3 and os.path.exists(sys.argv[3]):
        dates = json.load(open(sys.argv[3], encoding='utf-8'))

    articles, seen = [], set()
    for name in sorted(os.listdir(src)):
        if not name.endswith('.md'):
            continue
        path = os.path.join(src, name)
        raw  = open(path, encoding='utf-8').read()
        if len(raw.strip()) < 200:
            print('  atlandı (çok kısa):', name); continue

        title, body, tags = parse(raw)
        date = dates.get(name) or datetime.fromtimestamp(
            os.path.getmtime(path), timezone.utc).isoformat()

        slug, base, n = slugify(title), slugify(title), 2
        while slug in seen:
            slug = f'{base}-{n}'; n += 1
        seen.add(slug)

        articles.append({
            'slug': slug, 'title': title, 'date': date,
            'tags': tags, 'content': body,
        })

    articles.sort(key=lambda a: a['date'], reverse=True)
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=1)

    print(f'{len(articles)} makale → {out}')
    for a in articles:
        print(f"  {a['date'][:10]}  {a['slug'][:50]:52} {len(a['tags'])} etiket")

if __name__ == '__main__':
    main()
