import tkinter as tk
import customtkinter as ctk

class AddTeamView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.controller = None

        self.heading = ctk.CTkLabel(
            self,
            text="Undefined",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        self.heading.pack(pady=(20, 12), anchor="w")

        self.image_frame = ctk.CTkFrame(self, fg_color=("gray90", "gray16"))
        self.image_frame.pack(fill="both") # set expand=True, pady=(4, 12) if you want it to take up entire screen even when there is no img
        self.image_label = tk.Label(
            self.image_frame,
            text="Undefined",
            background="#242424",
            foreground="white",
        )
        self.image_label.pack(fill="both", expand=True, padx=4, pady=4)

        self.capture_button = ctk.CTkButton(
            self,
            text="Undefined"
        )
        self.capture_button.pack(anchor="w", pady=(8, 8))
        self.camera_status = ctk.CTkLabel(self, text="Undefined")
        self.camera_status.pack(anchor="w", pady=(0, 12))

        self.pit_scouting_grid = ctk.CTkFrame(self, height=90, corner_radius=8)
        self.pit_scouting_grid.pack(fill="x", expand=False, pady=(0, 12))

        self.match_grid = ctk.CTkScrollableFrame(self, height=220, orientation = "vertical", corner_radius=8)
        self.match_grid.pack(fill="both", expand=True, pady=(0, 12))

    def set_controller(self, controller):
        self.controller = controller 
        self.capture_button.configure(command=controller.open_camera)

    def add_team(self):
        self.controller.reset_state()
        self.heading.configure(text="Add Team")
        self.capture_button.configure(text="Scan QR Code")
        self.camera_status.configure(text="")

    def edit_team(self, team_number):
        self.controller.reset_state()
        self.heading.configure(text=f"Edit Team #{team_number}")
        self.capture_button.configure(text="Retake QR Code")
        self.camera_status.configure(text="Scan the team's QR code to quickly update the in-app database with any new information.")

        self.controller.load_team(team_number)

    def display_team_matches(self, matches):
        for child in self.match_grid.winfo_children():
            child.destroy()
        
        if not matches:
            ctk.CTkLabel(self.match_grid, text="No match data found.").grid(
                row=1, column=0, columnspan=2, sticky="w", padx=8, pady=6
            )
            return

        headings = [
            "Match",
            "Auton Fuel Scored",
            "Teleop Fuel Scored",
            "No Show",
            "Robot Disabled",
            "Beached",
            "Stuck on Bump",
            "Other Problem",
            "Climbed"
        ]

        for col, heading in enumerate(headings):
            #self.match_grid.grid_columnconfigure(col, weight=1)
            ctk.CTkLabel(self.match_grid, text=heading, font=ctk.CTkFont(weight="bold")).grid(
                row=0, column=col, sticky="w", padx=8, pady=6
            )

        for row, match in enumerate(matches, start=1):
            ctk.CTkLabel(self.match_grid, text=str(match.match_number)).grid(
                row=row, column=0, sticky="w", padx=8, pady=4
            )
            ctk.CTkLabel(self.match_grid, text=str(match.auton_fuel_scored)).grid(
                row=row, column=1, sticky="w", padx=8, pady=4
            )
            ctk.CTkLabel(self.match_grid, text=str(match.teleop_fuel_scored)).grid(
                row=row, column=2, sticky="w", padx=8, pady=4
            )
            ctk.CTkLabel(self.match_grid, text="Yes" if match.no_show else "No").grid(
                row=row, column=3, sticky="w", padx=8, pady=4
            )
            ctk.CTkLabel(self.match_grid, text="Yes" if match.robot_disabled else "No").grid(
                row=row, column=4, sticky="w", padx=8, pady=4
            )
            ctk.CTkLabel(self.match_grid, text="Yes" if match.beached else "No").grid(
                row=row, column=5, sticky="w", padx=8, pady=4
            )
            ctk.CTkLabel(self.match_grid, text="Yes" if match.stuck_on_bump else "No").grid(
                row=row, column=6, sticky="w", padx=8, pady=4
            )
            ctk.CTkLabel(self.match_grid, text="Yes" if match.other_problem else "No").grid(
                row=row, column=7, sticky="w", padx=8, pady=4
            )
            ctk.CTkLabel(self.match_grid, text="Yes" if match.climbed else "No").grid(
                row=row, column=8, sticky="w", padx=8, pady=4
            )
    
    def display_team_pit_scouting(self, pit_scouting):
        for child in self.pit_scouting_grid.winfo_children():
            child.destroy()
        
        if not pit_scouting:
            ctk.CTkLabel(self.pit_scouting_grid, text="No pit scouting data found.").grid(
                row=1, column=0, columnspan=2, sticky="w", padx=8, pady=6
            )
            return

        headings = [
            "Team Number",
            "Robot Weight",
            "Robot Length",
            "Robot Height",
            "Can Climb",
            "Drive Train Type",
            "Shooter Type",
            "Max Fuel Capacity"
        ]

        for col, heading in enumerate(headings):
            ctk.CTkLabel(self.pit_scouting_grid, text=heading, font=ctk.CTkFont(weight="bold")).grid(
                row=0, column=col, sticky="w", padx=8, pady=6
            )

        ctk.CTkLabel(self.pit_scouting_grid, text=str(pit_scouting.team_number)).grid(
            row=1, column=0, sticky="w", padx=8, pady=4
        )
        ctk.CTkLabel(self.pit_scouting_grid, text=str(pit_scouting.robot_weight)).grid(
            row=1, column=1, sticky="w", padx=8, pady=4
        )
        ctk.CTkLabel(self.pit_scouting_grid, text=str(pit_scouting.robot_length)).grid(
            row=1, column=2, sticky="w", padx=8, pady=4
        )
        ctk.CTkLabel(self.pit_scouting_grid, text=str(pit_scouting.robot_height)).grid(
            row=1, column=3, sticky="w", padx=8, pady=4
        )
        ctk.CTkLabel(self.pit_scouting_grid, text="Yes" if pit_scouting.can_climb else "No").grid(
            row=1, column=4, sticky="w", padx=8, pady=4
        )
        ctk.CTkLabel(self.pit_scouting_grid, text=str(pit_scouting.drive_train_type)).grid(
            row=1, column=5, sticky="w", padx=8, pady=4
        )
        ctk.CTkLabel(self.pit_scouting_grid, text=str(pit_scouting.shooter_type)).grid(
            row=1, column=6, sticky="w", padx=8, pady=4
        )
        ctk.CTkLabel(self.pit_scouting_grid, text=str(pit_scouting.max_fuel_capacity)).grid(
            row=1, column=7, sticky="w", padx=8, pady=4
        )
    