import customtkinter as ctk


class MainView(ctk.CTkFrame):
    def __init__(self, parent, controller, view_names):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.nav_buttons = {}

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        ctk.CTkLabel(
            self.sidebar_frame,
            text="Scouting App",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).grid(row=0, column=0, padx=20, pady=(20, 10))

        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        for row, view_name in enumerate(view_names, start=1):
            button = ctk.CTkButton(
                self.sidebar_frame,
                text=view_name,
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                anchor="w",
                command=lambda name=view_name: self.controller.navigate_to(name),
            )
            button.grid(row=row, column=0, sticky="ew", padx=20, pady=5)
            self.nav_buttons[view_name] = button

    def set_active_view(self, name):
        for view_name, button in self.nav_buttons.items():
            button.configure(
                fg_color=("gray70", "gray30") if view_name == name else "transparent"
            )

    