from contextlib import closing

from models.pit_scouting_model import PitScoutingModel
from database.database import get_connection

# see match scouting repo bro
# also see pit scouting model for wierd definitions
class PitScoutingRepository:
    @staticmethod
    def _from_row(row):
        return PitScoutingModel(
            team_number=row["team_number"],
            robot_weight=row["robot_weight"],
            robot_length=row["robot_length"],
            robot_height=row["robot_height"],
            can_climb=bool(row["can_climb"]),
            drive_train_type=row["drive_train_type"],
            shooter_type=row["shooter_type"],
            max_fuel_capacity=row["max_fuel_capacity"]
        )

    @staticmethod
    def _values(team: PitScoutingModel):
        return (
            team.team_number,
            team.robot_weight,
            team.robot_length,
            team.robot_height,
            team.can_climb,
            team.drive_train_type,
            team.shooter_type,
            team.max_fuel_capacity
        )

    def add(self, team: PitScoutingModel):
        with closing(get_connection()) as connection:
            with connection:
                connection.execute(
                    """
                    INSERT INTO pit_scouting (
                        team_number, robot_weight, robot_length, robot_height,
                        can_climb, drive_train_type, shooter_type, max_fuel_capacity
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    self._values(team)
                )
    
    def remove(self, team_number: int):
        with closing(get_connection()) as connection:
            with connection:
                connection.execute(
                    """
                    DELETE FROM pit_scouting WHERE team_number = ?
                    """,
                    (team_number,)
                )
    
    def edit(self, team_number: int, updated_team: PitScoutingModel):
        with closing(get_connection()) as connection:
            with connection:
                connection.execute(
                    """
                    UPDATE pit_scouting
                    SET team_number = ?, robot_weight = ?, robot_length = ?, robot_height = ?,
                        can_climb = ?, drive_train_type = ?, shooter_type = ?, max_fuel_capacity = ?
                    WHERE team_number = ?
                    """,
                    (*self._values(updated_team), team_number)
                )

    def get_all(self):
        with closing(get_connection()) as connection:
            with connection:
                cursor = connection.execute(
                    """
                    SELECT * FROM pit_scouting
                    """
                )
                return [self._from_row(row) for row in cursor.fetchall()]

    def get_team(self, team_number: int):
        with closing(get_connection()) as connection:
            with connection:
                cursor = connection.execute(
                    """
                    SELECT * FROM pit_scouting WHERE team_number = ?
                    """,
                    (team_number,)
                )
                return self._from_row(row) if (row := cursor.fetchone()) is not None else None
