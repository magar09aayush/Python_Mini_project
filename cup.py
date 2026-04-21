# cup.py
# Represents the hockey cup event itself.
# Holds metadata about the tournament (VG-level requirement).

class Cup:
    """Stores information about the hockey cup tournament."""

    def __init__(self, name: str, location: str, sport_type: str,
                 start_date: str, end_date: str, description: str):
        """
        Args:
            name       : Name of the cup/tournament.
            location   : City where the event is held.
            sport_type : Type of sport event (e.g. 'Ice Hockey').
            start_date : Start date in YYYY-MM-DD format.
            end_date   : End date in YYYY-MM-DD format.
            description: Short description of the event.
        """
        self.__name = name
        self.__location = location
        self.__sport_type = sport_type
        self.__start_date = start_date
        self.__end_date = end_date
        self.__description = description

    # ── Getters ──────────────────────────────────────────────────────────────

    def get_name(self) -> str:
        return self.__name

    def get_location(self) -> str:
        return self.__location

    def get_sport_type(self) -> str:
        return self.__sport_type

    def get_start_date(self) -> str:
        return self.__start_date

    def get_end_date(self) -> str:
        return self.__end_date

    def get_description(self) -> str:
        return self.__description

    # ── Display ───────────────────────────────────────────────────────────────

    def __str__(self) -> str:
        return (
            f"\n{'='*50}\n"
            f"  Cup Name   : {self.__name}\n"
            f"  Location   : {self.__location}\n"
            f"  Sport      : {self.__sport_type}\n"
            f"  Dates      : {self.__start_date} → {self.__end_date}\n"
            f"  Description: {self.__description}\n"
            f"{'='*50}"
        )