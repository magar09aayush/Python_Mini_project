# team.py
# Represents a single hockey team in the cup registration system.
# Each team object holds all relevant data about a team.

from datetime import date


class Team:
    """Represents a hockey team registered for the cup."""

    # Class-level fee variable — the participation fee every team must pay.
    # This is a class variable because the fee is the same for all teams.
    PARTICIPATION_FEE = 500  # SEK

    def __init__(self, team_id: int, name: str, team_type: str, fee_paid: bool = False):
        """
        Initialize a new Team object.

        Args:
            team_id  : Unique integer ID assigned by the repository.
            name     : Name of the team.
            team_type: 'boys' or 'girls'.
            fee_paid : Whether the participation fee has been paid (default False).
        """
        # Private attributes — accessed only via getters/setters (encapsulation)
        self.__id = team_id
        self.__date_created = date.today().strftime("%Y-%m-%d")
        self.__name = name
        self.__type = team_type.lower()
        self.__fee_paid = fee_paid
        self.__cancelled = False
        self.__cancellation_date = None   # Format: YYYY-MM-DD (set when cancelled)

    # ── Getters ──────────────────────────────────────────────────────────────

    def get_id(self) -> int:
        return self.__id

    def get_date_created(self) -> str:
        return self.__date_created

    def get_name(self) -> str:
        return self.__name

    def get_type(self) -> str:
        return self.__type

    def is_fee_paid(self) -> bool:
        return self.__fee_paid

    def is_cancelled(self) -> bool:
        return self.__cancelled

    def get_cancellation_date(self):
        return self.__cancellation_date

    # ── Setters ──────────────────────────────────────────────────────────────

    def set_name(self, name: str):
        self.__name = name

    def set_type(self, team_type: str):
        self.__type = team_type.lower()

    def set_fee_paid(self, status: bool):
        self.__fee_paid = status

    def cancel(self):
        """Mark the team as cancelled and record today as the cancellation date."""
        self.__cancelled = True
        self.__cancellation_date = date.today().strftime("%Y-%m-%d")

    def uncancel(self):
        """Reverse a cancellation."""
        self.__cancelled = False
        self.__cancellation_date = None

    # ── Serialisation helpers (used by TeamStorage) ───────────────────────────

    def to_dict(self) -> dict:
        """Convert the team to a dictionary for JSON serialisation."""
        return {
            "id": self.__id,
            "date_created": self.__date_created,
            "name": self.__name,
            "type": self.__type,
            "fee_paid": self.__fee_paid,
            "cancelled": self.__cancelled,
            "cancellation_date": self.__cancellation_date,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Team":
        """Reconstruct a Team from a dictionary (loaded from file)."""
        team = cls(
            team_id=data["id"],
            name=data["name"],
            team_type=data["type"],
            fee_paid=data["fee_paid"],
        )
        # Restore fields that the constructor cannot set directly
        team._Team__date_created = data["date_created"]
        team._Team__cancelled = data["cancelled"]
        team._Team__cancellation_date = data["cancellation_date"]
        return team

    # ── Display ───────────────────────────────────────────────────────────────

    def __str__(self) -> str:
        fee_status = "Paid" if self.__fee_paid else "Unpaid"
        cancelled_info = f"  | CANCELLED on {self.__cancellation_date}" if self.__cancelled else ""
        return (
            f"ID: {self.__id:>4}  |  {self.__name:<25}  |  "
            f"Type: {self.__type:<6}  |  Fee: {fee_status:<6}  |  "
            f"Registered: {self.__date_created}{cancelled_info}"
        )