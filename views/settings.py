import customtkinter as ctk


class SettingsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        ctk.CTkLabel(
            self,
            text="Settings",
            font=ctk.CTkFont(size=24, weight="bold"),
        ).pack(pady=(20, 16), anchor="w")
        ctk.CTkLabel(self, text="Appearance").pack(anchor="w", pady=(8, 6))

        self.appearance = ctk.CTkSegmentedButton(
            self,
            values=["System", "Light", "Dark"],
            command=ctk.set_appearance_mode,
        )
        self.appearance.set(ctk.get_appearance_mode())
        self.appearance.pack(anchor="w")