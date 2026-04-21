# team_storage.py
# Handles saving and loading team data to/from a JSON file.
# Collaborates with: Team (serialises/deserialises Team objects),
#                    TeamRepository (provides/receives the team list).

import json
import os
from team import Team


class TeamStorage:
    """Persists team data to a JSON file so data survives between sessions."""

    def __init__(self, filepath: str = "teams_data.json"):
        """
        Args:
            filepath: Path to the JSON file used for storage.
        """
        self.__filepath = filepath

    # ── Save ──────────────────────────────────────────────────────────────────

    def save(self, teams: list):
        """
        Serialise a list of Team objects and write them to the JSON file.
        Called automatically after every add / update / delete (auto-save).
        """
        data = [team.to_dict() for team in teams]
        try:
            with open(self.__filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"[Storage] Error saving data: {e}")

    # ── Load ──────────────────────────────────────────────────────────────────

    def load(self) -> list:
        """
        Read the JSON file and return a list of Team objects.
        Returns an empty list if the file does not exist or is empty.
        """
        if not os.path.exists(self.__filepath):
            return []
        try:
            with open(self.__filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [Team.from_dict(item) for item in data]
        except (IOError, json.JSONDecodeError) as e:
            print(f"[Storage] Error loading data: {e}")
            return []

    # ── CSV export (advanced bonus feature) ──────────────────────────────────

    def export_csv(self, teams: list, csv_path: str = "teams_export.csv"):
        """Export all team data to a CSV file."""
        try:
            with open(csv_path, "w", encoding="utf-8") as f:
                f.write("id,date_created,name,type,fee_paid,cancelled,cancellation_date\n")
                for t in teams:
                    d = t.to_dict()
                    f.write(
                        f"{d['id']},{d['date_created']},{d['name']},"
                        f"{d['type']},{d['fee_paid']},{d['cancelled']},"
                        f"{d['cancellation_date'] or ''}\n"
                    )
            print(f"[Storage] Teams exported to '{csv_path}'.")
        except IOError as e:
            print(f"[Storage] Error exporting CSV: {e}")