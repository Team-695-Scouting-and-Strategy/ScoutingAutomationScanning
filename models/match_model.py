# stores the data of one team for one match
# as a result there will be 6 of these per matches



class MatchModel:
    def __init__(self, team_number, match_number, auton_fuel_scored, teleop_fuel_scored, no_show, robot_disabled, beached, stuck_on_bump, other_problem, climbed):
        # identification
        self.team_number = team_number
        self.match_number = match_number

        # ints
        self.auton_fuel_scored = auton_fuel_scored
        self.teleop_fuel_scored = teleop_fuel_scored

        # bools
        self.no_show = no_show
        self.robot_disabled = robot_disabled
        self.beached = beached
        self.stuck_on_bump = stuck_on_bump
        self.other_problem = other_problem
        self.climbed = climbed


    
    
  