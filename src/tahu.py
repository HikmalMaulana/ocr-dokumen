import cv2
import os

# Path folder berisi gambar
folder_path = r"C:\Users\Lenovo\Downloads\ocr-dokumen\src\data"

def resize_for_display(image, max_width=500):
    h, w = image.shape[:2]
    if w > max_width:
        scale = max_width / w
        image = cv2.resize(image, (int(w * scale), int(h * scale)))
    return image

# Ekstensi yang diterima
valid_ext = (".jpg")

# Ambil semua file gambar
image_files = [
    f for f in os.listdir(folder_path)
    if f.lower().endswith(valid_ext)
]

if len(image_files) == 0:
    raise ValueError("Tidak ada gambar di folder")

for filename in image_files:
    image_path = os.path.join(folder_path, filename)
    image = cv2.imread(image_path)

    if image is None:
        print(f"Gagal membaca {filename}")
        continue
    display = resize_for_display(image, max_width=500)
    cv2.imshow("Input Image", display)
    cv2.waitKey(0)   # tekan apa saja untuk lanjut ke gambar berikutnya

cv2.destroyAllWindows()
