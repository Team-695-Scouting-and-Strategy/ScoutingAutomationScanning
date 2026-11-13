import cv2
from dataclasses import dataclass

@dataclass
class QRCodeData:
    qr_text: str

image_path = ""
image = cv2.imread(image_path)

if image is None:
    raise FileNotFoundError("Image could not be loaded.")

image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# detect the QR code
detector = cv2.QRCodeDetector()
qr_text, points, _ = detector.detectAndDecode(image)

data = QRCodeData(qr_text)

print("QR contents:", data.qr_text)