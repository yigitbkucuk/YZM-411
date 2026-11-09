# YZM 411 - Ödev #1: Renk, Aydınlatma ve Örnekleme

Bu çalışma; sabit bir masaüstü sahnesinde farklı aydınlatma koşullarının (Normal, Gölge, Lamba) renk uzayları (RGB ve HSV) üzerindeki etkilerini, piksel düzeyinde parlaklık/gama dönüşümlerini ve uzamsal küçültme/büyütme işlemlerindeki bilgi kayıplarını deneysel olarak incelemektedir.

---

## Çalışma Kapsamı ve Hedefler

1. **Görüntünün Sayısal Yapısı (Hedef 1):**
   * Normal, Gölge ve Lamba aydınlatması altında 3 farklı sahne piksellerinin (Kupa, Kağıt, Kitap) RGB değerlerinin analizi.
2. **Renk Eşikleri ve Aydınlatma duyarlılığı (Hedef 2):**
   * Sabit RGB ve HSV eşiklerinin 3 farklı ışık koşulunda uygulanması.
   * **6 Farklı Renk Maskesi** oluşturulması ve alan oranlarının (%) karşılaştırılması.
3. **Parlaklık ve Gama Dönüşümleri (Hedef 3):**
   * Parlaklık artırımı (`+40`) ve Gama dönüşümlerinin (`γ = 0.5`, `γ = 2.0`) piksel ortalamalarına ve doygunluk kırpılmasına (saturation clipping) etkisi.
4. **Uzamsal Örnekleme ve Interpolasyon (Hedef 4):**
   * Metin içeren bölgenin $1/4$ oranında küçültülüp 4x büyütülmesi (`INTER_NEAREST` ve `INTER_AREA`).
   * Bilgi kaybının Nyquist Örnekleme Teoremi çerçevesinde açıklanması.

---

## Rapor ve Sayfa Sayısı Notu

* **Taslak:** IEEE Çift Sütunlu (Two-Column) Şablonu.
* **Sayfa Düzeni Hakkında Not:** Ödev yönergesinde raporun 2 sayfa olması hedeflenmiştir. Ancak analizde istenen **6 adet renk maskesi**, **3 piksel RGB analiz tablosu**, **maske oranları karşılaştırma tablosu**, **parlaklık/gama grafikleri** ve **uzamsal örnekleme kesitlerinin** görsellerinin okunabilirliğini ve netliğini korumak; IEEE sütun yapısının bozulmasını önlemek amacıyla rapor **3 sayfa** olarak düzenlenmiştir[cite: 3, 4, 5].

---

## Klasör Yapısı

```text
YZM_411_Odev_1/
│
├── data/                                         # Orijinal girdi fotoğrafları
│   ├── normal.jpg
│   ├── golge.jpg
│   └── lamba.jpg
│
├── outputs/                                      # İşlenmiş çıktı görselleri ve maskeler
│   ├── renk_maskeleri.png
│   ├── parlaklik_gama_donusumleri.png
│   └── kucultme_ornekleme.png
│
├── main.py                                       # Tüm deneysel analizleri çalıştıran Python kodu
├── requirements.txt                              # Gerekli bağımlılıklar
├── YZM411_Odev1_Yiğit_Buğra_Küçük_230212048.pdf  # Final Ödev Raporu (PDF)
└── README.md                                     # Ödev açıklama belgesi
```

## Çalıştırma Talimatları

**1. Gerekli kütüphaneleri yükleyin:**

pip install -r requirements.txt

**2. Analiz kodunu çalıştırın:**

python main.py
