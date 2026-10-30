import tkinter as tk

import customtkinter as ctk

from camera import Camera
from image_utils import load_preview_image


class AddMatchPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.camera = Camera(self.winfo_toplevel(), on_capture=self._on_capture)
        self.current_match_path = None
        self.preview_image = None

        self.heading = ctk.CTkLabel(
            self,
            text="Add Match",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        self.heading.pack(pady=(20, 12), anchor="w")

        self.image_frame = ctk.CTkFrame(self, fg_color=("gray90", "gray16"))
        self.image_frame.pack(fill="both", expand=True, pady=(4, 12))
        self.image_label = tk.Label(
            self.image_frame,
            text="No scouting paper captured",
            background="#242424",
            foreground="white",
        )
        self.image_label.pack(fill="both", expand=True, padx=4, pady=4)

        self.capture_button = ctk.CTkButton(
            self,
            text="Take Picture",
            command=self.open_camera,
        )
        self.capture_button.pack(anchor="w", pady=(0, 8))
        self.camera_status = ctk.CTkLabel(self, text="")
        self.camera_status.pack(anchor="w", pady=(0, 12))

    def load_match(self, image_path=None):
        self.current_match_path = image_path
        if image_path is None:
            self.heading.configure(text="Add Match")
            self.capture_button.configure(text="Take Picture")
            self.camera_status.configure(text="")
            self.image_label.configure(image="", text="No scouting paper captured")
            self.image_label.image = None
            self.preview_image = None
            return

        self.heading.configure(text="Edit Match")
        self.capture_button.configure(text="Retake Picture")
        self.camera_status.configure(text="Retake the scouting photo to replace it.")
        self._show_image(image_path)

    def open_camera(self):
        self.camera.show_video(output_path=self.current_match_path)

    def _show_image(self, image_path):
        self.preview_image = load_preview_image(image_path, (640, 360))
        if self.preview_image is None:
            self.image_label.configure(image="", text="Could not load this picture")
        else:
            self.image_label.configure(image=self.preview_image, text="")
        self.image_label.image = self.preview_image

    def _on_capture(self, filename):
        self.current_match_path = filename
        self.heading.configure(text="Edit Match")
        self.capture_button.configure(text="Retake Picture")
        self.camera_status.configure(text="Picture captured. Retake it any time.")
        self._show_image(filename)