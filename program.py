# program.py
# Entry point for the Hockey Cup Registration System.
# Initialises all components and starts the user interface.

from cup import Cup
from team_repository import TeamRepository
from team_storage import TeamStorage
from user_interface import UserInterface


def main():
    """Set up the system and launch the CLI menu."""

    # Define the cup/tournament details
    cup = Cup(
        name="Dalarna Winter Cup 2026",
        location="Borlange",
        sport_type="Ice Hockey",
        start_date="Start:- 2026-03-18",
        end_date="End:- 2026-03-24",
        description="Annual youth hockey tournament in the heart of Dalarna."
    )

    # Create the repository (in-memory store) and storage (file persistence)
    repository = TeamRepository()
    storage = TeamStorage(filepath="teams_data.json")

    # Create the UI and hand it the dependencies
    ui = UserInterface(repository, storage, cup)

    # Start the interactive menu
    ui.run()


if __name__ == "__main__":
    main()