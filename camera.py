import base64
import time
import tkinter as tk

import cv2
import customtkinter as ctk
import zxingcpp

class Camera:
    SCAN_CONFIRM_SECONDS = 0.5

    def __init__(self, parent, on_scan=None):
        self.parent = parent
        self.on_scan = on_scan
        self.window = None
        self.preview_label = None
        self.status = None
        self.camera_menu = None
        self.capture = None
        self.after_id = None
        self.preview_image = None
        self.camera_options = {}
        self.pending_qr_text = None
        self.qr_detected_at = None
        self.scan_status = None

    @staticmethod
    def list_cameras(max_index=10):
        """Return camera indexes that OpenCV can open."""
        available = []
        for camera_id in range(max_index):
            device = cv2.VideoCapture(camera_id)
            if device.isOpened():
                available.append(camera_id)
            device.release()
        return available

    def show_video(self):
        if self.window is not None and self.window.winfo_exists():
            self.window.focus()
            return

        self.window = ctk.CTkToplevel(self.parent)
        self.window.title("Camera Preview")
        self.window.geometry("760x560")
        self.window.minsize(520, 400)
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=1)
        self.window.protocol("WM_DELETE_WINDOW", self.close)

        controls = ctk.CTkFrame(self.window, fg_color="transparent")
        controls.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))
        controls.grid_columnconfigure(0, weight=1)

        self.camera_menu = ctk.CTkOptionMenu(
            controls,
            values=["Searching for cameras..."],
            command=self._select_camera,
        )
        self.camera_menu.grid(row=0, column=0, sticky="w", padx=(0, 8))
        ctk.CTkButton(
            controls,
            text="Refresh cameras",
            command=self.refresh_cameras,
        ).grid(row=0, column=1, sticky="e")

        preview = ctk.CTkFrame(
            self.window,
            fg_color=("gray90", "gray16"),
            corner_radius=8,
        )
        preview.grid(row=1, column=0, sticky="nsew", padx=16, pady=8)
        self.preview_label = tk.Label(
            preview,
            text="Searching for cameras...",
            background="#242424",
            foreground="white",
        )
        self.preview_label.pack(fill="both", expand=True, padx=4, pady=4)

        footer = ctk.CTkFrame(self.window, fg_color="transparent")
        footer.grid(row=2, column=0, sticky="ew", padx=16, pady=(8, 16))
        footer.grid_columnconfigure(0, weight=1)
        self.status = ctk.CTkLabel(footer, text="")
        self.status.grid(row=0, column=0, sticky="w")
        ctk.CTkButton(
            footer,
            text="Exit",
            fg_color="transparent",
            border_width=1,
            command=self.close,
        ).grid(row=0, column=1)

        self.refresh_cameras()

    def refresh_cameras(self):
        self._release_camera()
        camera_ids = self.list_cameras()
        self.camera_options = {f"Camera {camera_id}": camera_id for camera_id in camera_ids}

        if not camera_ids:
            self.camera_menu.configure(values=["No cameras found"], state="disabled")
            self.preview_label.configure(image="", text="No cameras found")
            self.status.configure(text="Connect a camera and refresh the list.")
            return

        labels = list(self.camera_options)
        self.camera_menu.configure(values=labels, state="normal")
        selected_label = labels[0]
        self.camera_menu.set(selected_label)
        self._open_camera(self.camera_options[selected_label])

    def _select_camera(self, label):
        camera_id = self.camera_options.get(label)
        if camera_id is not None:
            self._open_camera(camera_id)

    def _open_camera(self, camera_id):
        self._release_camera()
        self.capture = cv2.VideoCapture(camera_id)
        if not self.capture.isOpened():
            self._release_camera()
            self.status.configure(text=f"Could not open Camera {camera_id}.")
            self.preview_label.configure(image="", text="Camera unavailable")
            return

        self.status.configure(text=f"Showing Camera {camera_id}")
        self.pending_qr_text = None
        self.qr_detected_at = None
        self.scan_status = None
        self.after_id = self.window.after(15, self._update_preview)

    def _update_preview(self):
        self.after_id = None
        if self.window is None or not self.window.winfo_exists() or self.capture is None:
            return

        success, frame = self.capture.read()
        if not success:
            self.status.configure(text="Unable to read from this camera.")
            self._release_camera()
            self.preview_label.configure(image="", text="Camera feed unavailable")
            return

        barcodes = zxingcpp.read_barcodes(
            frame,
            formats=zxingcpp.BarcodeFormat.QRCode,
        )
        barcode = barcodes[0] if barcodes else None
        qr_text = barcode.text if barcode else None

        if barcode:
            position = barcode.position
            corners = [
                position.top_left,
                position.top_right,
                position.bottom_right,
                position.bottom_left,
            ]
            for start, end in zip(corners, corners[1:] + corners[:1]):
                cv2.line(
                    frame,
                    (start.x, start.y),
                    (end.x, end.y),
                    (60, 220, 80),
                    3,
                )

        if qr_text:
            if qr_text != self.pending_qr_text:
                self.pending_qr_text = qr_text
                self.qr_detected_at = time.monotonic()
            elif time.monotonic() - self.qr_detected_at >= self.SCAN_CONFIRM_SECONDS:
                self.status.configure(text="QR code scanned.")
                self.close()
                if self.on_scan is not None:
                    self.on_scan(qr_text)
                return
            self._set_scan_status("QR code detected. Hold it steady...")
        else:
            self.pending_qr_text = None
            self.qr_detected_at = None
            self._set_scan_status("Center a QR code in the camera view.")

        preview_width = self.preview_label.winfo_width()
        preview_height = self.preview_label.winfo_height()
        if preview_width > 1 and preview_height > 1:
            preview_frame = cv2.resize(
                frame,
                (preview_width, preview_height),
                interpolation=cv2.INTER_AREA,
            )
        else:
            preview_frame = frame
        encoded, image_data = cv2.imencode(".png", preview_frame)
        if encoded:
            image = base64.b64encode(image_data).decode("ascii")
            self.preview_image = self._photo_image(image)
            self.preview_label.configure(image=self.preview_image, text="")

        self.after_id = self.window.after(15, self._update_preview)

    @staticmethod
    def _photo_image(image_data):
        return tk.PhotoImage(data=image_data)

    def _set_scan_status(self, text):
        if text != self.scan_status:
            self.status.configure(text=text)
            self.scan_status = text

    def _release_camera(self):
        if self.after_id is not None and self.window is not None:
            try:
                self.window.after_cancel(self.after_id)
            except Exception:
                pass
            self.after_id = None
        if self.capture is not None:
            self.capture.release()
            self.capture = None
        self.pending_qr_text = None
        self.qr_detected_at = None

    def close(self):
        self._release_camera()
        if self.window is not None and self.window.winfo_exists():
            self.window.destroy()
        self.window = None




