#!/usr/bin/env python3
"""
Arşivin coğrafi kapsamını gösterir.

Amaç: hangi bölgelere hiç bakılmadığını görünür kılmak. Yazı seçimi
yalnızca "aklıma ne gelirse" ile yapılırsa kaynakların yoğun olduğu
coğrafyalar (Batı Avrupa, Kuzey Amerika) doğal olarak öne çıkar.
Bu betik o eğilimi ölçülebilir hale getirir.

Kullanım: python3 bolgeler.py
"""
import json, os, collections

HERE = os.path.dirname(os.path.abspath(__file__))

# Yer etiketi → bölge eşlemesi. Yeni etiketler eklendikçe buraya yazılmalı;
# eşlenmeyenler raporun sonunda ayrıca listelenir.
BOLGE = {
 'Doğu Asya':            ['#çin', '#japonya', '#kore', '#tayvan', '#moğolistan'],
 'Güneydoğu Asya':       ['#vietnam', '#tayland', '#endonezya', '#filipinler', '#malezya'],
 'Güney Asya':           ['#hindistan', '#nepal', '#srilanka', '#pakistan', '#tibet'],
 'Orta Asya':            ['#ortaasya', '#kazakistan', '#özbekistan', '#afganistan'],
 'Sibirya ve Kuzey':     ['#sibirya', '#rusya', '#grönland', '#izlanda'],
 'Anadolu':              ['#anadolu', '#istanbul'],
 'Yakın Doğu ve İran':   ['#ortadoğu', '#iran', '#mezopotamya', '#suriye', '#arabistan'],
 'Kuzey Afrika':         ['#mısır', '#magrip', '#etiyopya'],
 'Sahra Altı Afrika':    ['#namibya', '#kongo', '#nijerya', '#güneyafrika', '#tanzanya'],
 'Akdeniz Antikitesi':   ['#roma', '#yunanistan', '#kartaca'],
 'Batı ve Orta Avrupa':  ['#ingiltere', '#fransa', '#almanya', '#avrupa', '#ispanya',
                          '#italya', '#hollanda', '#isviçre', '#avusturya', '#belçika'],
 'Kuzey Avrupa':         ['#iskandinavya', '#norveç', '#isveç', '#finlandiya', '#danimarka'],
 'Doğu Avrupa':          ['#polonya', '#macaristan', '#balkanlar', '#ukrayna'],
 'Kuzey Amerika':        ['#abd', '#kanada', '#alaska'],
 'Mezoamerika':          ['#meksika', '#guatemala'],
 'Güney Amerika':        ['#peru', '#and', '#brezilya', '#arjantin', '#amerika'],
 'Karayipler':           ['#karayipler', '#kuba', '#haiti'],
 'Avustralya':           ['#avustralya'],
 'Okyanusya':            ['#polinezya', '#yenizelanda', '#hawaii', '#pasifik'],
 'Kutuplar':             ['#antarktika', '#kutup'],
}

def main():
    a = json.load(open(os.path.join(HERE, 'articles.json'), encoding='utf-8'))
    say = collections.Counter(k for x in a for k in x['tags'] if k.startswith('#'))

    tersi = {e: b for b, ler in BOLGE.items() for e in ler}
    bolge_say = collections.Counter()
    for e, n in say.items():
        bolge_say[tersi.get(e, '__bilinmeyen__')] += n

    bilinmeyen = sorted(e for e in say if e not in tersi)

    sirali = sorted(BOLGE, key=lambda b: (bolge_say[b], b))
    bos  = [b for b in sirali if bolge_say[b] == 0]
    zayif = [b for b in sirali if 0 < bolge_say[b] <= 2]

    print(f'ARŞİV: {len(a)} yazı, {len(say)} yer etiketi\n')
    print('BÖLGE KAPSAMI (az kapsanandan çoğa)')
    for b in sirali:
        n = bolge_say[b]
        isaret = '·' if n == 0 else '█' * n
        print(f'  {b:22} {n:2}  {isaret}')

    print()
    if bos:
        print('HİÇ YAZI OLMAYAN BÖLGELER:')
        for b in bos:
            print(f'  · {b}')
    if zayif:
        print('\nZAYIF KALAN BÖLGELER (1-2 yazı):')
        for b in zayif:
            print(f'  · {b}')
    if bilinmeyen:
        print('\nEŞLEMEYE EKLENMESİ GEREKEN ETİKETLER:')
        print('  ' + ', '.join(bilinmeyen))

if __name__ == '__main__':
    main()
