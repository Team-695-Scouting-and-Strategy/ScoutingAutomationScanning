import base64
import tkinter as tk

import cv2


def load_preview_image(path, size):
    frame = cv2.imread(str(path))
    if frame is None:
        return None

    width, height = size
    scale = min(width / frame.shape[1], height / frame.shape[0])
    resized = cv2.resize(
        frame,
        (int(frame.shape[1] * scale), int(frame.shape[0] * scale)),
        interpolation=cv2.INTER_AREA,
    )
    vertical = height - resized.shape[0]
    horizontal = width - resized.shape[1]
    padded = cv2.copyMakeBorder(
        resized,
        vertical // 2,
        vertical - vertical // 2,
        horizontal // 2,
        horizontal - horizontal // 2,
        cv2.BORDER_CONSTANT,
        value=(36, 36, 36),
    )
    encoded, image_data = cv2.imencode(".png", padded)
    if not encoded:
        return None
    image_data_base64 = base64.b64encode(image_data).decode("ascii")
    return tk.PhotoImage(data=image_data_base64)