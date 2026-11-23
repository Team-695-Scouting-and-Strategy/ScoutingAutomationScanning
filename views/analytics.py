import customtkinter as ctk

class AnalyticsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.controller = None

        self.heading = ctk.CTkLabel(
            self,
            text="Analytics",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        self.heading.pack(pady=(20, 12), anchor="w")

        self.info_label = ctk.CTkLabel(
            self,
            text="Analytics features will be implemented here.",
            font=ctk.CTkFont(size=16),
        )
        self.info_label.pack(pady=(0, 12), anchor="w")