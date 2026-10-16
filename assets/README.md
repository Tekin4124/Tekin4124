# Profil görselleri

Sade tipografi ve projelerin işlevlerinden türetilmiş hareketli arayüz çizimleri.
Stok ikon, iletişim kartı, harici istatistik servisi veya takip yok.

- Başlık sabittir. Beş proje satırının her biri ayrı animasyondur.
- Masaüstü 1280 × 278; mobil 800 × 550. GitHub picture/media ile uygun
  düzeni seçer. Hareket azaltma tercihinde statik sürümler gösterilir.
- Animasyonlar 120 kaynak kare, 50 ms/kare, 6 saniye; tam periyotlu döngü. Aynı kalan kareler süreleri korunarak birleştirilir.
- Arayüz çizimleri işlevleri temsil eder; gerçek ürün kaydı veya restorasyon
  kalite karşılaştırması değildir. İlan, sipariş ve takvim içerikleri sentetiktir.
- Üretim: Python 3 + Pillow, `python3 tools/render_profile.py`. Font yolları
  betiğin başındadır (Nimbus Sans Bold / DejaVu Sans Mono).

Önceki tasarım: `profile-before-motion-2026-10-16` Git etiketi.
