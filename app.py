import customtkinter as ctk

from database.database import initialize_database

from views import VIEW_REGISTRY
from views.main_view import MainView

from controllers.dashboard_controller import DashboardController
from controllers.add_team_controller import AddTeamController

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Scouting App")
        self.geometry("800x500")
        self.main_view = MainView(self, controller=self, view_names=VIEW_REGISTRY)
        self.main_view.pack(fill="both", expand=True)

        content_frame = self.main_view.content_frame

        dashboard_view = VIEW_REGISTRY["Dashboard"](parent=content_frame)
        self.dashboard_controller = DashboardController(dashboard_view, self)
        dashboard_view.set_controller(self.dashboard_controller)

        add_team_view = VIEW_REGISTRY["Add Team"](parent=content_frame)
        self.add_team_controller = AddTeamController(add_team_view, self)
        add_team_view.set_controller(self.add_team_controller)

        self.frames = {
            "Dashboard": dashboard_view,
            "Add Team": add_team_view,
            "Settings": VIEW_REGISTRY["Settings"](parent=content_frame),
            "Analytics": VIEW_REGISTRY["Analytics"](parent=content_frame),
        }

        self.select_frame(next(iter(VIEW_REGISTRY)))

    def select_frame(self, name):
        self.main_view.set_active_view(name)
        frame = self.frames[name]
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()

    def navigate_to(self, name):
        if name == "Add Team":
            self.open_add_team()
        else:
            self.select_frame(name)

    def open_add_team(self):
        self.frames["Add Team"].add_team()
        self.select_frame("Add Team")

    def open_edit_team(self, team_number):
        self.frames["Add Team"].edit_team(team_number)
        self.select_frame("Add Team")

if __name__ == "__main__":
    initialize_database()
    app = MainApplication()
    app.mainloop()
