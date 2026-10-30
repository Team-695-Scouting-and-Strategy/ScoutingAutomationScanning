import customtkinter as ctk
from pages import PAGE_REGISTRY

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Scouting App")
        self.geometry("800x500")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="My App",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.nav_buttons = {}
        for row, (page_name, page_class) in enumerate(PAGE_REGISTRY.items(), start=1):
            button_command = (
                self.open_new_match
                if page_name == "Add Match"
                else lambda name=page_name: self.select_frame(name)
            )
            button = ctk.CTkButton(
                self.sidebar_frame,
                text=page_name,
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                anchor="w",
                command=button_command,
            )
            button.grid(row=row, column=0, sticky="ew", padx=20, pady=5)
            self.nav_buttons[page_name] = button
            self.frames[page_name] = page_class(
                parent=self.container,
                controller=self,
            )

        self.select_frame(next(iter(PAGE_REGISTRY)))

    def select_frame(self, name):
        for page_name, button in self.nav_buttons.items():
            button.configure(
                fg_color=("gray70", "gray30") if page_name == name else "transparent"
            )
        frame = self.frames[name]
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()

    def open_new_match(self):
        self.frames["Add Match"].load_match()
        self.select_frame("Add Match")

    def edit_match(self, image_path):
        self.frames["Add Match"].load_match(image_path)
        self.select_frame("Add Match")

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
