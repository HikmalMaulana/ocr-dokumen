import cv2
import os
import numpy as np
from imutils.perspective import four_point_transform

# =========================
# 1. PATH GAMBAR
# =========================
image_path = r"C:\Users\Lenovo\Downloads\ocr-dokumen\src\data\IMG-20251111-WA0040.jpg"

if not os.path.exists(image_path):
    raise FileNotFoundError("File gambar tidak ditemukan")

image = cv2.imread(image_path)
if image is None:
    raise ValueError("Gambar gagal dibaca")

# =========================
# 2. RESIZE UNTUK DISPLAY
# =========================
def resize_for_display(image, max_width=500):
    h, w = image.shape[:2]
    if w > max_width:
        scale = max_width / w
        image = cv2.resize(image, (int(w * scale), int(h * scale)))
    return image

# =========================
# 3. SCAN DOKUMEN (REFINED)
# =========================
def scan_document(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    _, threshold = cv2.threshold(
        blur, 0, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    contours, _ = cv2.findContours(
        threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    image_area = image.shape[0] * image.shape[1]

    for contour in contours:
        area = cv2.contourArea(contour)

        if area < 0.05 * image_area:
            continue

        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

        if len(approx) == 4:
            return four_point_transform(image, approx.reshape(4, 2))

    return None


# =========================
# 4. POST-PROCESSING SCAN
# =========================
def enhance_scan(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Adaptive threshold → lebih bersih
    scan = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    # Morphological operation → teks lebih tegas
    kernel = np.ones((2, 2), np.uint8)
    scan = cv2.morphologyEx(scan, cv2.MORPH_OPEN, kernel)

    return scan

# =========================
# 5. MAIN FLOW
# =========================
scanned = scan_document(image)

cv2.imshow("Original Image", resize_for_display(image))

if scanned is not None:
    cv2.imshow("Scanned (Perspective Fixed)", resize_for_display(scanned))

    final_scan = enhance_scan(scanned)

    # Crop ringan (lebih aman)
    h, w = final_scan.shape
    final_scan = final_scan[5:h-5, 5:w-5]

    cv2.imshow("Final Scan", resize_for_display(final_scan))
else:
    print("⚠️ Dokumen tidak terdeteksi")

cv2.waitKey(0)
cv2.destroyAllWindows()