from contextlib import closing

from models.match_model import MatchModel
from database.database import get_connection

# repository layer between database and controller
# implements basic operations like
# add, remove, edit, get_all, get_by_id, get_by_team_number, get_by_match_number, get_by_team_and_match_number, etc. and allat jazz
class MatchScoutingRepository:
    @staticmethod
    def _from_row(row):
        return MatchModel(
            team_number=row["team_number"],
            match_number=row["match_number"],
            auton_fuel_scored=row["auton_fuel_scored"],
            teleop_fuel_scored=row["teleop_fuel_scored"],
            no_show=bool(row["no_show"]),
            robot_disabled=bool(row["robot_disabled"]),
            beached=bool(row["beached"]),
            stuck_on_bump=bool(row["stuck_on_bump"]),
            other_problem=bool(row["other_problem"]),
            climbed=bool(row["climbed"]),
        )

    @staticmethod
    def _values(match: MatchModel):
        return (
            match.team_number,
            match.match_number,
            match.auton_fuel_scored,
            match.teleop_fuel_scored,
            match.no_show,
            match.robot_disabled,
            match.beached,
            match.stuck_on_bump,
            match.other_problem,
            match.climbed,
        )

    def add(self, match: MatchModel):
        with closing(get_connection()) as connection:
            with connection:
                connection.execute(
                    """
                    INSERT INTO match_scouting (
                        team_number, match_number, auton_fuel_scored, teleop_fuel_scored,
                        no_show, robot_disabled, beached, stuck_on_bump, other_problem, climbed
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    self._values(match)
                )
    
    def remove(self, match_id: int):
        with closing(get_connection()) as connection:
            with connection:
                connection.execute(
                    """
                    DELETE FROM match_scouting WHERE id = ?
                    """,
                    (match_id,)
                )

    def edit(self, match_id: int, updated_match: MatchModel):
        with closing(get_connection()) as connection:
            with connection:
                connection.execute(
                    """
                    UPDATE match_scouting
                    SET team_number = ?, match_number = ?, auton_fuel_scored = ?,
                        teleop_fuel_scored = ?, no_show = ?, robot_disabled = ?,
                        beached = ?, stuck_on_bump = ?, other_problem = ?, climbed = ?
                    WHERE id = ?
                    """,
                    (*self._values(updated_match), match_id)
                )

    def get_all(self):
        with closing(get_connection()) as connection:
            with connection:
                cursor = connection.execute(
                    """
                    SELECT * FROM match_scouting
                    """
                )
                return [self._from_row(row) for row in cursor.fetchall()]
    
    def get_all_teams(self):
        with closing(get_connection()) as connection:
            with connection:
                cursor = connection.execute(
                    """
                    SELECT DISTINCT team_number FROM match_scouting
                    """
                )
                return [row["team_number"] for row in cursor.fetchall()]

    def get_id_from_team_and_match_number(self, team_number: int, match_number: int):
        with closing(get_connection()) as connection:
            with connection:
                cursor = connection.execute(
                    """
                    SELECT id FROM match_scouting WHERE team_number = ? AND match_number = ?
                    """,
                    (team_number, match_number)
                )
                row = cursor.fetchone()
                if row:
                    return row["id"]
                return None

    def get_by_id(self, match_id: int):
        with closing(get_connection()) as connection:
            with connection:
                cursor = connection.execute(
                    """
                    SELECT * FROM match_scouting WHERE id = ?
                    """,
                    (match_id,)
                )
                row = cursor.fetchone()
                if row:
                    return self._from_row(row)
                return None

    def get_by_team_number(self, team_number: int):
        with closing(get_connection()) as connection:
            with connection:
                cursor = connection.execute(
                    """
                    SELECT * FROM match_scouting WHERE team_number = ?
                    """,
                    (team_number,)
                )
                return [self._from_row(row) for row in cursor.fetchall()]

    def get_by_match_number(self, match_number: int):
        with closing(get_connection()) as connection:
            with connection:
                cursor = connection.execute(
                    """
                    SELECT * FROM match_scouting WHERE match_number = ?
                    """,
                    (match_number,)
                )
                return [self._from_row(row) for row in cursor.fetchall()]

    def get_by_team_and_match_number(self, team_number: int, match_number: int):
        with closing(get_connection()) as connection:
            with connection:
                cursor = connection.execute(
                    """
                    SELECT * FROM match_scouting WHERE team_number = ? AND match_number = ?
                    """,
                    (team_number, match_number)
                )
                row = cursor.fetchone()
                if row:
                    return self._from_row(row)
                return None
    
