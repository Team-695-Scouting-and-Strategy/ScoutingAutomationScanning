from datetime import datetime
import tkinter as tk

import customtkinter as ctk

from camera import list_team_photos
from image_utils import load_preview_image


class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        ctk.CTkLabel(
            self,
            text="Dashboard",
            font=ctk.CTkFont(size=24, weight="bold"),
        ).pack(pady=(20, 8), anchor="w")
        ctk.CTkLabel(self, text="Saved scouting photos.").pack(anchor="w")

        self.match_list = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.match_list.pack(fill="both", expand=True, pady=(16, 8))

    def on_show(self):
        self.refresh_matches()

    def refresh_matches(self):
        for child in self.match_list.winfo_children():
            child.destroy()

        team_photos = list_team_photos()
        if not team_photos:
            ctk.CTkLabel(
                self.match_list,
                text="No matches yet. Add a match to capture a scouting paper.",
            ).pack(anchor="w", padx=8, pady=12)
            return

        for team_number, image_path in team_photos:
            self._add_photo_row(team_number, image_path)

    def _add_photo_row(self, team_number, image_path):
        item = ctk.CTkFrame(self.match_list, corner_radius=6)
        item.pack(fill="x", padx=4, pady=4)
        item.grid_columnconfigure(1, weight=1)

        thumbnail = load_preview_image(image_path, (140, 96))
        image_label = tk.Label(
            item,
            image=thumbnail,
            text="Image unavailable" if thumbnail is None else "",
            background="#242424",
            foreground="white",
        )
        image_label.image = thumbnail
        image_label.grid(row=0, column=0, rowspan=2, padx=8, pady=8)

        captured_at = datetime.fromtimestamp(image_path.stat().st_mtime)
        ctk.CTkLabel(
            item,
            text=f"Team {team_number}",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).grid(row=0, column=1, sticky="sw", padx=8, pady=(12, 2))
        ctk.CTkLabel(
            item,
            text=captured_at.strftime("Captured %b %d, %Y at %I:%M %p"),
        ).grid(row=1, column=1, sticky="nw", padx=8, pady=(2, 12))
        ctk.CTkButton(
            item,
            text="Edit",
            width=80,
            command=lambda path=image_path: self.controller.edit_match(path),
        ).grid(row=0, column=2, rowspan=2, padx=12, pady=12)