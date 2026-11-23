from repositories.match_scouting_repository import MatchScoutingRepository
from repositories.pit_scouting_repository import PitScoutingRepository
from models.match_model import MatchModel
from models.pit_scouting_model import PitScoutingModel
import random

class DashboardController:
    def __init__(self, view, main_app):
        self.main_app = main_app
        self.match_scouting_repository = MatchScoutingRepository()
        self.pit_scouting_repository = PitScoutingRepository()
        self.view = view
    
    def display_teams(self):
        teams = self.match_scouting_repository.get_all_teams()
        
        if not teams:
            self.view.show_no_teams_message()
        else:
            for team_number in teams:
                self.view.add_team_row(team_number)

    def edit_team(self, team_number):
        self.main_app.open_edit_team(team_number)

    def DEBUG_add_team(self):
        x = 0 if len(self.match_scouting_repository.get_all_teams()) == 0 else max(self.match_scouting_repository.get_all_teams())+1
        for i in range(10):              
            team = MatchModel(
                x, # team number
                x+i, # match number
                random.randint(0, 100),
                random.randint(0, 100),
                bool(random.randint(0, 1)),
                bool(random.randint(0, 1)),
                bool(random.randint(0, 1)),
                bool(random.randint(0, 1)),
                bool(random.randint(0, 1)),
                bool(random.randint(0, 1)),
            )
            self.match_scouting_repository.add(team)

        team_pit_scouting = PitScoutingModel(
            x,
            round(random.uniform(12, 36), 2),
            round(random.uniform(12, 36), 2),
            round(random.uniform(12, 36), 2),
            bool(random.randint(0, 1)),
            random.randint(0, 3),
            random.randint(0, 3),
            random.randint(10, 50)
        )
        self.pit_scouting_repository.add(team_pit_scouting)
        
                

    



    