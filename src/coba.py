import cv2
import os
import numpy as np
from imutils.perspective import four_point_transform
from PIL import Image
import io
import win32clipboard

CUSFILEPATH = {
     1 : r"C:\Users\Lenovo\Downloads\ocr-dokumen\src\data\IMG-20251111-WA0001.jpg",
     2 : r"C:\Users\Lenovo\Downloads\ocr-dokumen\src\data\IMG-20251111-WA0002.jpg",
     3 : r"C:\Users\Lenovo\Downloads\ocr-dokumen\src\data\IMG-20251111-WA0003.jpg",
     4 : r"C:\Users\Lenovo\Downloads\ocr-dokumen\src\data\IMG-20251111-WA0004.jpg",
     5 : r"C:\Users\Lenovo\Downloads\ocr-dokumen\src\data\IMG-20251111-WA0005.jpg",
     6 : r"C:\Users\Lenovo\Downloads\ocr-dokumen\src\data\IMG-20251111-WA0006.jpg",
     7 : r"C:\Users\Lenovo\Downloads\ocr-dokumen\src\data\IMG-20251111-WA0007.jpg",
     8 : r"C:\Users\Lenovo\Downloads\ocr-dokumen\src\data\IMG-20251111-WA0008.jpg",
     9 : r"C:\Users\Lenovo\Downloads\ocr-dokumen\src\data\IMG-20251111-WA0009.jpg",
     10 : r"C:\Users\Lenovo\Downloads\ocr-dokumen\src\data\IMG-20251111-WA0010.jpg",
     11 : r"C:\Users\Lenovo\Downloads\ocr-dokumen\src\data\IMG-20251111-WA0011.jpg",
     12 : r"C:\Users\Lenovo\Downloads\ocr-dokumen\src\data\IMG-20251111-WA0012.jpg",
     13 : r"C:\Users\Lenovo\Downloads\ocr-dokumen\src\data\IMG-20251111-WA0013.jpg",
     14 : r"C:\Users\Lenovo\Downloads\ocr-dokumen\src\data\IMG-20251111-WA0014.jpg",
     15 : r"C:\Users\Lenovo\Downloads\ocr-dokumen\src\data\IMG-20251111-WA0015.jpg",
     16 : r"C:\Users\Lenovo\Downloads\ocr-dokumen\src\data\IMG-20251111-WA0016.jpg",
     17 : r"C:\Users\Lenovo\Downloads\ocr-dokumen\src\data\IMG-20251111-WA0017.jpg",
}

#from cusfile import *
# =========================
# 1. PATH GAMBAR
# =========================
image_path = CUSFILEPATH[1]
def image_processing(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
    return threshold

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
# 3. FUNGSI SCAN DOKUMEN
# =========================
def scan_document(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    thresh = cv2.adaptiveThreshold(
        blur, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    contours, _ = cv2.findContours(
        thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
    )
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 5000:
            continue
        
        peri = cv2.arcLength(contour, True)
        
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
        

        if len(approx) == 4:
            return image
            
    return None


def copy_image_to_clipboard(img):
    # OpenCV (BGR) → PIL (RGB)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)

    output = io.BytesIO()
    pil_img.save(output, format="BMP")
    data = output.getvalue()[14:]  # skip BMP header
    output.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()




cv2.imshow("Original Image", resize_for_display(image))
scanned = scan_document(image)


if scanned is not None:
    # 1. Post-processing
    processed = image_processing(scanned)
    processed = processed[10:-10, 10:-10]

    # 2. Tampilkan hasil
    cv2.imshow("Processed", resize_for_display(processed))

    # >>> DI SINI <<<
    copy_image_to_clipboard(processed)
    print("✅ Hasil scan disalin ke clipboard (Ctrl+V siap)")

else:
    print("⚠️ Dokumen tidak terdeteksi")

cv2.waitKey(0)
cv2.destroyAllWindows()


cv2.waitKey(0)
cv2.destroyAllWindows()