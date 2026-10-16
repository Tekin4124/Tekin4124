# Profil görselleri

Özgün, Pillow ile yerel çizilmiş tipografi ve temsili proje akışları.

- Başlık: ortalanmış isim, harflere çarpan top, raket, parçacıklar ve
  topu takip eden zemin ışıkları; 180 kaynak kare, 50 ms/kare,
  9 saniyelik döngü. README içinde oynanabilir JavaScript değil, GIF animasyonudur.
- Yükio: üç farklı mesajın rota, araç ve tonaj alanları ayrışır; tamamlanan
  ilanlar akışa yerleşerek öncekileri aşağı taşır. Altta mesajın rotası izlenir.
  Bütün hareketler kendi paneline kırpılır.
- NoteFlow: siyah defter, yazı, vurgu ve gölgeli sayfa çevirme. Sayfa aynı
  menteşe etrafında ileri ve geri çevrilir; döngü sonunda kare sıfırlanmaz.
  Cilt halkaları hareket boyunca sabit kalır.
- Diğer üç proje animasyonu korunur. Masaüstü 1280 × 278, mobil 800 × 550.
- Projeler: 120 kaynak kare, 50 ms/kare, 6 saniye. Aynı karelerin süreleri
  korunarak birleştirilir. Hareket azaltma tercihinde sabit sürümler gösterilir.
- Görseller temsili arayüz çizimleridir; gerçek ürün kaydı veya restorasyon
  kalite karşılaştırması değildir. İçerikler sentetiktir.
- Üretim: Python 3 + Pillow, `python3 tools/render_profile.py`. Yalnız seçili
  projeler için `--only yukio noteflow`; font yolları betiğin başındadır.

Önceki sürüm: `profile-before-refinement-2026-10-16` Git etiketi.
