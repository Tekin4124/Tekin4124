# Profil görselleri

Özgün, Pillow ile yerel çizilmiş tipografi ve temsili proje akışları.

- Başlık: ismin harflerine çarpan top ve raket; 180 kaynak kare, 50 ms/kare,
  9 saniyelik döngü. README içinde oynanabilir JavaScript değil, GIF animasyonudur.
- Yükio: mesajdan rota, araç ve tonaj alanlarının ilan kartına sırayla aktarımı.
  Bütün hareketler kendi paneline kırpılır; dışarı taşan çizgi bulunmaz.
- NoteFlow: yazı, vurgu, cilt ve gölgeli/perspektifli sayfa çevirme.
- Diğer üç proje animasyonu korunur. Masaüstü 1280 × 278, mobil 800 × 550.
- Projeler: 120 kaynak kare, 50 ms/kare, 6 saniye. Aynı karelerin süreleri
  korunarak birleştirilir. Hareket azaltma tercihinde sabit sürümler gösterilir.
- Görseller temsili arayüz çizimleridir; gerçek ürün kaydı veya restorasyon
  kalite karşılaştırması değildir. İçerikler sentetiktir.
- Üretim: Python 3 + Pillow, `python3 tools/render_profile.py`. Yalnız seçili
  projeler için `--only yukio noteflow`; font yolları betiğin başındadır.

Önceki sürüm: `profile-before-arcade-2026-10-16` Git etiketi.
