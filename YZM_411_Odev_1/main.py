import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


# 1. KLASÖR VE DOSYA YOLLARI

DATA_DIR = "data"
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

img_paths = {
    "normal": os.path.join(DATA_DIR, "normal.jpg"),
    "golge": os.path.join(DATA_DIR, "golge.jpg"),
    "lamba": os.path.join(DATA_DIR, "lamba.jpg")
}


# 2. ADIM 3: İŞLEMDEN ÖNCE TAHMİNLER

print("### ADIM 3: İŞLEMDEN ÖNCE TAHMİNLER ###")
print("Tahmin 1 (Hedef 1): Normal ışıkta kahverengi bardakta R baskın iken beyaz kağıtta R,G,B birbirine yakın ve yüksek çıkacaktır. Gölgede tüm noktaların RGB değerleri düşecek; lamba altında renk sıcaklığı değişecektir.")
print("Tahmin 2 (Hedef 2): Gölgede piksel değerleri düşeceği için sabit RGB eşiklerimizin kapladığı alan oranı küçülecektir. HSV uzayındaki Ton (H) kanalı aydınlatmaya dayanıklı olduğu için HSV maskesi daha kararlı kalacaktır.")
print("Tahmin 3 (Hedef 3): +40 parlaklık artışında ortalama yaklaşık 40 artacaktır. Gama 0.5 görüntüyü aydınlatırken Gama 2.0 belirgin şekilde karartacaktır.")
print("Tahmin 4 (Hedef 4): 1/4 küçültmede küçük yazı detayları kaybolacaktır. INTER_NEAREST yöntemi pikselleşme ve sahte desen (aliasing) üretecek, INTER_AREA yöntemi ise alan ortalaması alarak yazıyı griye dönüştürüp bulanıklaştıracaktır.\n")


# 3. GÖRÜNTÜLERİ YÜKLEME VE DÖNÜŞÜMLER (HEDEF 1)

images_bgr = {}
images_rgb = {}
images_hsv = {}

for key, path in img_paths.items():
    if not os.path.exists(path):
        raise FileNotFoundError(f"HATA: {path} bulunamadı.")
    bgr_img = cv2.imread(path)
    images_bgr[key] = bgr_img
    images_rgb[key] = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
    images_hsv[key] = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)

sample_img = images_rgb["normal"]
height, width, channels = sample_img.shape

print("### GÖRÜNTÜ SAYISAL YAPISI (NORMAL IŞIK) ###")
print(f"Boyut: {height}x{width}x{channels}, Tür: {sample_img.dtype}, Değer Aralığı: [{sample_img.min()}, {sample_img.max()}]\n")


# 4. HEDEF 1: FARKLI BÖLGELERDEN 3 PİKSEL ANALİZİ

points = {
    "Piksel 1 (Kahverengi Kupa)": (int(height * 0.65), int(width * 0.40)),
    "Piksel 2 (Beyaz Kağıt)   ": (int(height * 0.85), int(width * 0.25)),
    "Piksel 3 (Kitap Kapağı)  ": (int(height * 0.30), int(width * 0.70))
}

print("### SEÇİLEN 3 FARKLI PİKSELİN ÖLÇÜMLERİ ###")
for p_name, (py, px) in points.items():
    print(f"--- {p_name} [y={py}, x={px}] ---")
    for key in ["normal", "golge", "lamba"]:
        r, g, b = images_rgb[key][py, px]
        print(f"  {key.capitalize():8s} Işık -> R: {r:3d}, G: {g:3d}, B: {b:3d}")
print("\n")


# 5. HEDEF 2: SABİT RENK EŞİKLERİ VE MASKELER

lower_rgb = np.array([50, 20, 10])
upper_rgb = np.array([140, 90, 70])
lower_hsv = np.array([0, 30, 20])
upper_hsv = np.array([25, 200, 160])

masks, ratios = {}, {}
for key in ["normal", "golge", "lamba"]:
    rgb_mask = cv2.inRange(images_rgb[key], lower_rgb, upper_rgb)
    hsv_mask = cv2.inRange(images_hsv[key], lower_hsv, upper_hsv)
    masks[f"{key}_rgb"] = rgb_mask
    masks[f"{key}_hsv"] = hsv_mask
    ratios[f"{key}_rgb"] = (np.sum(rgb_mask == 255) / rgb_mask.size) * 100
    ratios[f"{key}_hsv"] = (np.sum(hsv_mask == 255) / hsv_mask.size) * 100

print("### MASKE ALAN ORANLARI (%) ###")
for k, v in ratios.items():
    print(f"{k.upper():12s}: %{v:.3f}")
print("\n")

fig, axes = plt.subplots(3, 2, figsize=(10, 12))
mask_keys = [("normal_rgb", "normal_hsv"), ("golge_rgb", "golge_hsv"), ("lamba_rgb", "lamba_hsv")]
for idx, (rgb_k, hsv_k) in enumerate(mask_keys):
    axes[idx, 0].imshow(masks[rgb_k], cmap='gray')
    axes[idx, 0].set_title(f"{rgb_k.upper()} (%{ratios[rgb_k]:.2f})")
    axes[idx, 0].axis('off')
    axes[idx, 1].imshow(masks[hsv_k], cmap='gray')
    axes[idx, 1].set_title(f"{hsv_k.upper()} (%{ratios[hsv_k]:.2f})")
    axes[idx, 1].axis('off')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "renk_maskeleri.png"))
plt.close()


# 6. HEDEF 3: PARLAKLIK VE GAMA DÖNÜŞÜMLERİ

img_float = sample_img.astype(np.float32)

brightness_img = np.clip(img_float + 40.0, 0, 255).astype(np.uint8)
gamma_05_img = np.clip(255.0 * ((img_float / 255.0) ** 0.5), 0, 255).astype(np.uint8)
gamma_20_img = np.clip(255.0 * ((img_float / 255.0) ** 2.0), 0, 255).astype(np.uint8)

orig_mean = np.mean(sample_img)
bright_mean = np.mean(brightness_img)
g05_mean = np.mean(gamma_05_img)
g20_mean = np.mean(gamma_20_img)

# 255'te doyuma ulaşan (patlayan) piksel analizi
saturated_pixels = np.sum((img_float + 40.0) > 255.0)
total_pixels_count = sample_img.shape[0] * sample_img.shape[1] * sample_img.shape[2]

print("### PARLAKLIK VE GAMA ÖLÇÜMLERİ ###")
print(f"Orijinal Ortalama        : {orig_mean:.2f}")
print(f"Parlaklık (+40) Ortalama : {bright_mean:.2f} (Beklenen: {orig_mean + 40:.2f}, Fark: {(orig_mean + 40) - bright_mean:.2f})")
print(f"255'te Doyuma Ulaşan Piksel Sayısı: {saturated_pixels} / {total_pixels_count} (%{(saturated_pixels/total_pixels_count)*100:.4f})")
print(f"Gama (gamma=0.5) Ortalama: {g05_mean:.2f}")
print(f"Gama (gamma=2.0) Ortalama: {g20_mean:.2f}\n")

fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes[0, 0].imshow(sample_img)
axes[0, 0].set_title(f"Orijinal (Ort: {orig_mean:.1f})")
axes[0, 0].axis('off')

axes[0, 1].imshow(brightness_img)
axes[0, 1].set_title(f"Parlaklik +40 (Ort: {bright_mean:.1f})")
axes[0, 1].axis('off')

axes[1, 0].imshow(gamma_05_img)
axes[1, 0].set_title(f"Gama 0.5 (Ort: {g05_mean:.1f})")
axes[1, 0].axis('off')

axes[1, 1].imshow(gamma_20_img)
axes[1, 1].set_title(f"Gama 2.0 (Ort: {g20_mean:.1f})")
axes[1, 1].axis('off')

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "parlaklik_gama_donusumleri.png"))
plt.close()


# 7. HEDEF 4: KÜÇÜLTME VE UZAMSAL ÖRNEKLEME

crop_text = sample_img[int(height * 0.05):int(height * 0.35), int(width * 0.55):int(width * 0.95)]

down_nearest = cv2.resize(crop_text, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_NEAREST)
down_area = cv2.resize(crop_text, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)

up_nearest = cv2.resize(down_nearest, (crop_text.shape[1], crop_text.shape[0]), interpolation=cv2.INTER_NEAREST)
up_area = cv2.resize(down_area, (crop_text.shape[1], crop_text.shape[0]), interpolation=cv2.INTER_NEAREST)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].imshow(crop_text)
axes[0].set_title("Orijinal Kesit")
axes[0].axis('off')

axes[1].imshow(up_nearest)
axes[1].set_title("INTER_NEAREST (1/4 -> 4x)")
axes[1].axis('off')

axes[2].imshow(up_area)
axes[2].set_title("INTER_AREA (1/4 -> 4x)")
axes[2].axis('off')

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "kucultme_ornekleme.png"))
plt.close()

print("İşlemler tamamlandı. Üretilen tüm görseller 'outputs/' klasörüne kaydedildi.")