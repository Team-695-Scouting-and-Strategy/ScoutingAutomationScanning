# stores the data of one team from pit scouting
# there should be only one per team

class PitScoutingModel:
    def __init__(self, team_number, robot_weight, robot_length, robot_height, can_climb, drive_train_type, shooter_type, max_fuel_capacity):
        self.team_number = team_number
        self.robot_weight = robot_weight
        self.robot_length = robot_length
        self.robot_height = robot_height
        self.can_climb = can_climb
        self.drive_train_type = drive_train_type # (swerve=0, tank=1, other=2, none=3)
        self.shooter_type = shooter_type # (turret=0, fixed=1, other=2, none=3)
        self.max_fuel_capacity = max_fuel_capacity