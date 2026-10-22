import cv2
import pytesseract
from dataclasses import dataclass

@dataclass
class QRCodeData:
    qr_text: str
    extracted_text: str 

image_path = "" # paste path of scouting form image here
image = cv2.imread(image_path)

if image is None:
    raise FileNotFoundError("Image could not be loaded.")

image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# detect the QR code
detector = cv2.QRCodeDetector()
qr_text, points, _ = detector.detectAndDecode(image)

if points is not None:
    points = points.reshape(-1, 2)

    # find QR code boundaries
    x1 = int(points[:, 0].min())
    y1 = int(points[:, 1].min())
    x2 = int(points[:, 0].max())
    y2 = int(points[:, 1].max())

    # cropping the area to the right of the QR code
    height, width = image.shape[:2]
    crop = image_rgb[
        max(0, y1 - 20):min(height, y2 + 100),
        min(width, x2 + 5):min(width, x2 + 350)
    ]

    # extracting the text from the image
    extracted_text = pytesseract.image_to_string(crop).strip()

    # storing in class
    data = QRCodeData(qr_text, extracted_text)

    print(data)
    print("QR contents:", data.qr_text)
    print("Nearby text:", data.extracted_text)

else:
    print("No QR code detected.")