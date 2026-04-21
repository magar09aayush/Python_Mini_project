# team_repository.py
# Manages the collection of Team objects in memory.
# Responsible for adding, retrieving, updating, and deleting teams.
# Collaborates with: Team (creates/modifies Team objects).

from team import Team


class TeamRepository:
    """
    In-memory store for Team objects.
    Keeps a running counter to ensure IDs stay unique even after
    loading from file (maintained team ID requirement).
    """

    def __init__(self):
        # Dictionary mapping team_id -> Team object for O(1) lookups
        self.__teams: dict[int, Team] = {}
        # Next available ID; updated when teams are loaded from file
        self.__next_id: int = 1

    # ── ID management ─────────────────────────────────────────────────────────

    def _update_next_id(self):
        """Ensure __next_id is always higher than any existing ID."""
        if self.__teams:
            self.__next_id = max(self.__teams.keys()) + 1

    # ── CRUD ──────────────────────────────────────────────────────────────────

    def add_team(self, name: str, team_type: str, fee_paid: bool = False) -> Team:
        """Create a new team, store it, and return the object."""
        team = Team(self.__next_id, name, team_type, fee_paid)
        self.__teams[self.__next_id] = team
        self.__next_id += 1
        return team

    def get_team_by_id(self, team_id: int):
        """Return the Team with the given ID, or None if not found."""
        return self.__teams.get(team_id)

    def get_all_teams(self) -> list:
        """Return all teams as a list."""
        return list(self.__teams.values())

    def get_teams_by_type(self, team_type: str) -> list:
        """Return teams filtered by 'boys' or 'girls'."""
        return [t for t in self.__teams.values()
                if t.get_type() == team_type.lower()]

    def update_team(self, team_id: int, name: str = None,
                    team_type: str = None, fee_paid: bool = None) -> bool:
        """
        Update one or more attributes of a team.
        Returns True if the team was found and updated, False otherwise.
        """
        team = self.get_team_by_id(team_id)
        if team is None:
            return False
        if name is not None:
            team.set_name(name)
        if team_type is not None:
            team.set_type(team_type)
        if fee_paid is not None:
            team.set_fee_paid(fee_paid)
        return True

    def cancel_team(self, team_id: int) -> bool:
        """Cancel a team. Returns True on success."""
        team = self.get_team_by_id(team_id)
        if team is None:
            return False
        team.cancel()
        return True

    def delete_team(self, team_id: int) -> bool:
        """Permanently remove a team. Returns True on success."""
        if team_id in self.__teams:
            del self.__teams[team_id]
            return True
        return False

    # ── Search / filter ───────────────────────────────────────────────────────

    def search_by_name(self, keyword: str) -> list:
        """Return teams whose names contain the keyword (case-insensitive)."""
        kw = keyword.lower()
        return [t for t in self.__teams.values() if kw in t.get_name().lower()]

    def filter_by_payment(self, paid: bool) -> list:
        """Return teams filtered by fee-paid status."""
        return [t for t in self.__teams.values() if t.is_fee_paid() == paid]

    # ── Bulk load (used by TeamStorage) ───────────────────────────────────────

    def load_teams(self, teams: list):
        """Replace the current store with a list of Team objects loaded from file."""
        self.__teams = {t.get_id(): t for t in teams}
        self._update_next_id()

    # ── Statistics ────────────────────────────────────────────────────────────

    def get_statistics(self) -> dict:
        """Return a dict with basic statistics about all registered teams."""
        all_teams = self.get_all_teams()
        total = len(all_teams)
        paid = sum(1 for t in all_teams if t.is_fee_paid())
        cancelled = sum(1 for t in all_teams if t.is_cancelled())
        pct_paid = (paid / total * 100) if total > 0 else 0.0
        return {
            "total": total,
            "paid": paid,
            "unpaid": total - paid,
            "cancelled": cancelled,
            "pct_paid": round(pct_paid, 1),
        }