import cv2
import os

image_path = r"C:\Users\Lenovo\Downloads\ocr-dokumen\src\data\IMG-20251111-WA0039.jpg"

if not os.path.exists(image_path):
    raise FileNotFoundError("File gambar tidak ditemukan")

image = cv2.imread(image_path)
if image is None:
    raise ValueError("Gambar gagal dibaca")


def resize_for_display(image, max_width=500):
    h, w = image.shape[:2]
    if w > max_width:
        scale = max_width / w
        image = cv2.resize(image, (int(w * scale), int(h * scale)))
    return image


display = resize_for_display(image)

cv2.imshow("Input Image", display)
cv2.waitKey(0)
cv2.destroyAllWindows()
