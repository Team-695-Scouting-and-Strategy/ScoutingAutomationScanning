from repositories.match_scouting_repository import MatchScoutingRepository
from repositories.pit_scouting_repository import PitScoutingRepository
from camera import Camera

class AddTeamController:
    def __init__(self, view, main_app):
        self.main_app = main_app
        self.match_scouting_repository = MatchScoutingRepository()
        self.pit_scouting_repository = PitScoutingRepository()
        self.view = view
        self.view.camera = Camera(self.view.winfo_toplevel(), on_scan=self.on_qr_scanned)
    
    def open_camera(self):
        self.view.camera.show_video()

    def on_qr_scanned(self, text):
        self.view.current_qr_text = text
        self.view.image_label.configure(image="", text=text)
        self.view.image_label.image = None
        self.view.camera_status.configure(text="QR code scanned.")

    def reset_state(self):
        self.view.image_label.configure(text="No QR code captured")
        self.view.display_team_matches([])
        self.view.display_team_pit_scouting(None)

    # load team and draw in edit menu
    def load_team(self, team_number):
        matches = self.match_scouting_repository.get_by_team_number(team_number)
        self.view.display_team_matches(matches)

        pit_scouting_data = self.pit_scouting_repository.get_team(team_number)
        self.view.display_team_pit_scouting(pit_scouting_data)
