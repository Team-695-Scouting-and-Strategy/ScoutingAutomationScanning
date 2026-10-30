import base64
from datetime import datetime
from pathlib import Path
import re
import tkinter as tk

import cv2
import customtkinter as ctk

PICTURES_DIR = Path(__file__).resolve().parent / "pictures"


def list_team_photos():
    team_photos = []
    used_numbers = set()

    for path in PICTURES_DIR.glob("team_*.jpg"):
        match = re.match(r"team_(\d+)_", path.name)
        if match:
            team_number = int(match.group(1))
            team_photos.append((team_number, path))
            used_numbers.add(team_number)

    legacy_photos = sorted(PICTURES_DIR.glob("match_*.jpg"), key=lambda path: path.name)
    for path in legacy_photos:
        team_number = 1
        while team_number in used_numbers:
            team_number += 1
        team_photos.append((team_number, path))
        used_numbers.add(team_number)

    return sorted(team_photos, key=lambda entry: entry[0])


class Camera:
    def __init__(self, parent, on_capture=None):
        self.parent = parent
        self.on_capture = on_capture
        self.window = None
        self.preview = None
        self.preview_label = None
        self.status = None
        self.camera_menu = None
        self.capture = None
        self.after_id = None
        self.current_frame = None
        self.preview_image = None
        self.camera_options = {}
        self.output_path = None

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

    def show_video(self, output_path=None):
        if self.window is not None and self.window.winfo_exists():
            self.window.focus()
            return

        self.output_path = Path(output_path) if output_path else None
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

        self.preview = ctk.CTkFrame(
            self.window,
            fg_color=("gray90", "gray16"),
            corner_radius=8,
        )
        self.preview.grid(row=1, column=0, sticky="nsew", padx=16, pady=8)
        self.preview_label = tk.Label(
            self.preview,
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
            text="Take Picture",
            command=self.take_picture,
        ).grid(row=0, column=1, padx=(8, 8))
        ctk.CTkButton(
            footer,
            text="Exit",
            fg_color="transparent",
            border_width=1,
            command=self.close,
        ).grid(row=0, column=2)

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

        self.current_frame = frame
        preview_frame = cv2.resize(frame, (640, 360), interpolation=cv2.INTER_AREA)
        encoded, image_data = cv2.imencode(".png", preview_frame)
        if encoded:
            image = base64.b64encode(image_data).decode("ascii")
            self.preview_image = self._photo_image(image)
            self.preview_label.configure(image=self.preview_image, text="")

        self.after_id = self.window.after(15, self._update_preview)

    @staticmethod
    def _photo_image(image_data):
        return tk.PhotoImage(data=image_data)

    def take_picture(self):
        if self.current_frame is None:
            self.status.configure(text="No camera frame is available yet.")
            return

        try:
            PICTURES_DIR.mkdir(parents=True, exist_ok=True)
            output_path = self.output_path or self._new_team_path()
            if not cv2.imwrite(str(output_path), self.current_frame):
                self.status.configure(text="Could not save the picture. Check the pictures folder permissions.")
                return
        except (OSError, cv2.error) as error:
            self.status.configure(text=f"Could not save picture: {error}")
            return

        filename = str(output_path)
        self.close()
        if self.on_capture is not None:
            self.on_capture(filename)

    @staticmethod
    def _new_team_path():
        used_numbers = {team_number for team_number, _ in list_team_photos()}
        team_number = 1
        while team_number in used_numbers:
            team_number += 1
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        return PICTURES_DIR / f"team_{team_number}_{timestamp}.jpg"

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
        self.current_frame = None

    def close(self):
        self._release_camera()
        if self.window is not None and self.window.winfo_exists():
            self.window.destroy()
        self.window = None




