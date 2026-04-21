# user_interface.py
# Handles all user interaction through a command-line menu.
# Collaborates with: TeamRepository (all team CRUD operations),
#                    TeamStorage (save/load/export),
#                    Cup (displays cup info),
#                    Team (reads team data for display).

from team_repository import TeamRepository
from team_storage import TeamStorage
from cup import Cup
from team import Team


class UserInterface:
    """
    Command-line menu interface for the Hockey Cup registration system.
    All input/output happens here — business logic stays in the repository.
    """

    def __init__(self, repository: TeamRepository, storage: TeamStorage, cup: Cup):
        """
        Args:
            repository: The in-memory team store.
            storage   : Handles file persistence.
            cup       : The cup/tournament being administered.
        """
        self.__repo = repository
        self.__storage = storage
        self.__cup = cup

    # ── Auto-save helper ──────────────────────────────────────────────────────

    def __autosave(self):
        """Save all teams to file after every mutating operation."""
        self.__storage.save(self.__repo.get_all_teams())

    # ── Menu display ──────────────────────────────────────────────────────────

    def __print_header(self):
        print("\n" + "=" * 55)
        print(f" {self.__cup.get_name()}  —  Hockey Cup Manager")
        print("=" * 55)

    def __print_menu(self):
        self.__print_header()
        print("  1. Add new team")
        print("  2. View team by ID")
        print("  3. List all teams")
        print("  4. List boys teams")
        print("  5. List girls teams")
        print("  6. Update a team")
        print("  7. Cancel a team")
        print("  8. Delete a team")
        print("  9. Search teams by name")
        print(" 10. Filter teams by payment status")
        print(" 11. Show statistics")
        print(" 12. Show cup information")
        print(" 13. Export teams to CSV")
        print("  0. Exit")
        print("-" * 55)

    # ── Input helpers ─────────────────────────────────────────────────────────

    def __get_int(self, prompt: str):
        """Prompt until the user enters a valid integer."""
        while True:
            try:
                return int(input(prompt).strip())
            except ValueError:
                print("  ✗ Please enter a valid number.")

    def __get_team_type(self, prompt: str = "  Team type (boys/girls): ") -> str:
        """Prompt until 'boys' or 'girls' is entered."""
        while True:
            value = input(prompt).strip().lower()
            if value in ("boys", "girls"):
                return value
            print("  ✗ Please enter 'boys' or 'girls'.")

    def __get_yes_no(self, prompt: str) -> bool:
        """Prompt until y/n is entered. Returns True for 'y'."""
        while True:
            value = input(prompt).strip().lower()
            if value in ("y", "yes"):
                return True
            if value in ("n", "no"):
                return False
            print("  ✗ Please enter y or n.")

    # ── Feature handlers ──────────────────────────────────────────────────────

    def __add_team(self):
        print("\n── Add New Team ──────────────────────────")
        name = input("  Team name      : ").strip()
        if not name:
            print("  ✗ Name cannot be empty.")
            return
        team_type = self.__get_team_type()
        fee_paid = self.__get_yes_no("  Fee paid? (y/n): ")

        team = self.__repo.add_team(name, team_type, fee_paid)
        self.__autosave()
        print(f"\n  ✓ Team added successfully!")
        print(f"    {team}")
        print(f"    Participation fee: {Team.PARTICIPATION_FEE} SEK")

    def __view_team_by_id(self):
        print("\n── View Team by ID ───────────────────────")
        team_id = self.__get_int("  Enter team ID: ")
        team = self.__repo.get_team_by_id(team_id)
        if team:
            print(f"\n  {team}")
            print(f"  Participation fee: {Team.PARTICIPATION_FEE} SEK")
        else:
            print(f"  ✗ No team found with ID {team_id}.")

    def __list_teams(self, team_type: str = None):
        if team_type:
            teams = self.__repo.get_teams_by_type(team_type)
            label = f"{team_type.capitalize()} Teams"
        else:
            teams = self.__repo.get_all_teams()
            label = "All Teams"

        print(f"\n── {label} ({'──' * 10})")
        if not teams:
            print("  (no teams registered)")
            return
        for t in teams:
            print(f"  {t}")
        print(f"\n  Total shown: {len(teams)}")

    def __update_team(self):
        print("\n── Update Team ───────────────────────────")
        team_id = self.__get_int("  Enter team ID to update: ")
        team = self.__repo.get_team_by_id(team_id)
        if not team:
            print(f"  ✗ No team found with ID {team_id}.")
            return

        print(f"\n  Current data: {team}")
        print("  What to update?")
        print("    a. Name")
        print("    b. Gender/type")
        print("    c. Fee-paid status")
        choice = input("  Choose (a/b/c): ").strip().lower()

        if choice == "a":
            new_name = input("  New name: ").strip()
            if not new_name:
                print("  ✗ Name cannot be empty.")
                return
            self.__repo.update_team(team_id, name=new_name)
        elif choice == "b":
            new_type = self.__get_team_type("  New type (boys/girls): ")
            self.__repo.update_team(team_id, team_type=new_type)
        elif choice == "c":
            new_status = self.__get_yes_no("  Fee paid? (y/n): ")
            self.__repo.update_team(team_id, fee_paid=new_status)
        else:
            print("  ✗ Invalid choice.")
            return

        self.__autosave()
        print(f"  ✓ Team updated: {self.__repo.get_team_by_id(team_id)}")

    def __cancel_team(self):
        print("\n── Cancel Team ───────────────────────────")
        team_id = self.__get_int("  Enter team ID to cancel: ")
        team = self.__repo.get_team_by_id(team_id)
        if not team:
            print(f"  ✗ No team found with ID {team_id}.")
            return
        if team.is_cancelled():
            print("  ✗ This team is already cancelled.")
            return
        confirm = self.__get_yes_no(f"  Cancel team '{team.get_name()}'? (y/n): ")
        if confirm:
            self.__repo.cancel_team(team_id)
            self.__autosave()
            print(f"  ✓ Team '{team.get_name()}' has been cancelled.")
        else:
            print("  Cancelled — no changes made.")

    def __delete_team(self):
        print("\n── Delete Team ───────────────────────────")
        team_id = self.__get_int("  Enter team ID to delete: ")
        team = self.__repo.get_team_by_id(team_id)
        if not team:
            print(f"  ✗ No team found with ID {team_id}.")
            return
        confirm = self.__get_yes_no(f"  Permanently delete team '{team.get_name()}'? (y/n): ")
        if confirm:
            self.__repo.delete_team(team_id)
            self.__autosave()
            print(f"  ✓ Team deleted successfully.")
        else:
            print("  Cancelled — no changes made.")

    def __search_by_name(self):
        print("\n── Search by Name ────────────────────────")
        keyword = input("  Enter name keyword: ").strip()
        results = self.__repo.search_by_name(keyword)
        if not results:
            print(f"  No teams found matching '{keyword}'.")
        else:
            print(f"\n  Found {len(results)} team(s):")
            for t in results:
                print(f"  {t}")

    def __filter_by_payment(self):
        print("\n── Filter by Payment Status ──────────────")
        paid = self.__get_yes_no("  Show paid teams? (y = paid, n = unpaid): ")
        results = self.__repo.filter_by_payment(paid)
        label = "Paid" if paid else "Unpaid"
        if not results:
            print(f"  No {label.lower()} teams found.")
        else:
            print(f"\n  {label} teams ({len(results)}):")
            for t in results:
                print(f"  {t}")

    def __show_statistics(self):
        print("\n── Statistics ────────────────────────────")
        stats = self.__repo.get_statistics()
        fee = Team.PARTICIPATION_FEE
        collected = stats["paid"] * fee
        expected = stats["total"] * fee
        print(f"  Total teams registered : {stats['total']}")
        print(f"  Teams that paid        : {stats['paid']} ({stats['pct_paid']}%)")
        print(f"  Teams unpaid           : {stats['unpaid']}")
        print(f"  Cancelled teams        : {stats['cancelled']}")
        print(f"  Fee per team           : {fee} SEK")
        print(f"  Fees collected         : {collected} SEK / {expected} SEK expected")

    def __show_cup_info(self):
        print(self.__cup)

    def __export_csv(self):
        print("\n── Export to CSV ─────────────────────────")
        path = input("  CSV filename (press Enter for 'teams_export.csv'): ").strip()
        if not path:
            path = "teams_export.csv"
        self.__storage.export_csv(self.__repo.get_all_teams(), path)

    # ── Main loop ─────────────────────────────────────────────────────────────

    def run(self):
        """Start the interactive menu loop."""
        # Load existing data from file at startup
        loaded_teams = self.__storage.load()
        if loaded_teams:
            self.__repo.load_teams(loaded_teams)
            print(f"\n  [Info] Loaded {len(loaded_teams)} team(s) from file.")

        while True:
            self.__print_menu()
            choice = input("  Your choice: ").strip()

            if choice == "1":
                self.__add_team()
            elif choice == "2":
                self.__view_team_by_id()
            elif choice == "3":
                self.__list_teams()
            elif choice == "4":
                self.__list_teams("boys")
            elif choice == "5":
                self.__list_teams("girls")
            elif choice == "6":
                self.__update_team()
            elif choice == "7":
                self.__cancel_team()
            elif choice == "8":
                self.__delete_team()
            elif choice == "9":
                self.__search_by_name()
            elif choice == "10":
                self.__filter_by_payment()
            elif choice == "11":
                self.__show_statistics()
            elif choice == "12":
                self.__show_cup_info()
            elif choice == "13":
                self.__export_csv()
            elif choice == "0":
                print("\n  Goodbye! See you at the cup! \n")
                break
            else:
                print(" ✗ Invalid option. Please choose from the menu.")

            input("\n  Press Enter to continue...")