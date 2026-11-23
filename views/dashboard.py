import customtkinter as ctk

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.controller = None

        ctk.CTkButton(
            self,
            text="[DEBUG] Add random team match",
            font=ctk.CTkFont(size=24),
            command=lambda: self.controller.DEBUG_add_team(),
        ).pack(padx=10, pady=10, anchor="w")

        ctk.CTkLabel(
            self,
            text="Dashboard",
            font=ctk.CTkFont(size=24, weight="bold"),
        ).pack(pady=(20, 8), anchor="w")
        ctk.CTkLabel(self, text="Saved teams").pack(anchor="w")

        self.team_list = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.team_list.pack(fill="both", expand=True, pady=(16, 8))

    def set_controller(self, controller):
        self.controller = controller
    
    def on_show(self):
        self.refresh_teams()

    def refresh_teams(self):
        for child in self.team_list.winfo_children():
            child.destroy()

        self.controller.display_teams()

    def add_team_row(self, team_number):
        item = ctk.CTkFrame(self.team_list, corner_radius=6)
        item.pack(fill="x", padx=4, pady=4)
        item.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            item,
            text=f"Team {team_number}",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).grid(row=0, column=1, sticky="sw", padx=8, pady=(12, 2))
        ctk.CTkButton(
            item,
            text="Edit",
            width=80,
            command=lambda team_number=team_number: self.controller.edit_team(team_number),
        ).grid(row=0, column=2, rowspan=2, padx=12, pady=12)
        
    def show_no_teams_message(self):
        ctk.CTkLabel(
            self.team_list,
            text="No teams yet. Add a team by scanning a qr code from the app.",
        ).pack(anchor="w", padx=8, pady=12)