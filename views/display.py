import os
import platform
import time
from rich.console import Console
from rich.table import Table
from rich import box
from rich.panel import Panel


class Display:
    """Class to handle display operations such as logging messages and displaying tables"""
    def __init__(self):
        self.console = Console()

    def log(self):
        """ Welcome message"""
        epic_events = Panel(
            "[bold blue]CRM Epic Events",
            expand=False,
            border_style="blue",
            subtitle="Welcome",
            padding=(1, 8),
        )
        self.console.print(epic_events)
        print()

    def hello(self, firstname):
        """Display a greeting message to the user.

        Args:
            firstname (str): The first name of the user.
        """
        self.console.print(f"Bonjour {firstname}!", style="blue")
        time.sleep(2)
        self.clean()

    def display_table(self, result, table, all=False):
        """
        Display the results of queries in a table format.

        Args:
            result: The result of the query.
            table (str): The type of table to display.
            all (bool, optional): Indicates if there are multiple rows (True) or one row (False).
        """
        if table == "client":
            table_display = self.table_client(result, all)
        if table == "contract":
            table_display = self.table_contract(result, all)
        if table == "event":
            table_display = self.table_event(result, all)
        if table == "staff":
            table_display = self.table_staff(result, all)
        print()
        if table_display.rows:
            self.console.print(table_display)
        else:
            self.console.print("[i]Pas de résultat...[/i]", style="indian_red1")

        print()
        time.sleep(4)

    def table_client(self, result, all):
        """
        Construct the client table for display.

        Args:
            result: The result of the client query.
            all (bool): Indicates if there are multiple rows (True) or one row (False).

        Returns:
            Table: The constructed client table.
        """
        table_display = Table(title="Clients", show_lines=True, box=box.MINIMAL_DOUBLE_HEAD)
        table_display.add_column("Id", style="cyan", no_wrap=True)
        table_display.add_column("Nom complet", style="magenta", no_wrap=True)
        table_display.add_column("Email", style="green")
        table_display.add_column("Téléphone", style="cyan")
        table_display.add_column("Entreprise", style="magenta")
        table_display.add_column("Création", style="green")
        table_display.add_column("Mise à jour", style="green")
        table_display.add_column("Contact commercial", justify="right", style="cyan")
        if all:
            for row in result:
                table_display.add_row(
                    f"{row.id}",
                    f"{row.fullname}",
                    f"{row.email}",
                    f"{row.phone}",
                    f"{row.name_company}",
                    f"{row.date_creation}",
                    f"{row.date_update}",
                    f"{row.commercial_contact.first_name} {row.commercial_contact.name}",
                )

            return table_display
        else:
            table_display.add_row(
                f"{result.id}",
                f"{result.fullname}",
                f"{result.email}",
                f"{result.phone}",
                f"{result.name_company}",
                f"{result.date_creation}",
                f"{result.date_update}",
                f"{result.commercial_contact.first_name} {result.commercial_contact.name}",
            )
            return table_display

    def table_contract(self, result, all):
        """
        Construct the contract table for display.

        Args:
            result: The result of the contract query.
            all (bool): Indicates if there are multiple rows (True) or one row (False).

        Returns:
            Table: The constructed contract table.
        """
        table_display = Table(title="Contrats", show_lines=True, box=box.MINIMAL_DOUBLE_HEAD)
        table_display.add_column("Id", style="cyan", no_wrap=True)
        table_display.add_column("Client", style="magenta", no_wrap=True)
        table_display.add_column("Contact commercial", style="green")
        table_display.add_column("Total dû", style="cyan")
        table_display.add_column("Reste à payer", style="magenta")
        table_display.add_column("Création", style="green")
        table_display.add_column("Statut (signature)", style="green")

        if all:
            for row in result:
                table_display.add_row(
                    f"{row.id}",
                    f"{row.client.fullname}",
                    f"{row.commercial_contact.first_name} {row.commercial_contact.name}",
                    f"{row.total_amount}",
                    f"{row.balance_due}",
                    f"{row.date_creation}",
                    f"{row.status}",
                )

            return table_display
        else:
            table_display.add_row(
                f"{result.id}",
                f"{result.client.fullname}",
                f"{result.commercial_contact.first_name} {result.commercial_contact.name}",
                f"{result.total_amount}",
                f"{result.balance_due}",
                f"{result.date_creation}",
                f"{result.status}",
            )

            return table_display

    def table_event(self, result, all):
        """
        Construct the event table for display.

        Args:
            result: The result of the event query.
            all (bool): Indicates if there are multiple rows (True) or one row (False).

        Returns:
            Table: The constructed event table.
        """
        table_display = Table(
            title="Evènements",
            show_lines=True,
            box=box.MINIMAL_DOUBLE_HEAD,
            expand=True,
        )
        table_display.add_column("Id", style="cyan")
        table_display.add_column("Nom de l'évènement", style="cyan")
        table_display.add_column("Contrat (id)", style="magenta")
        table_display.add_column("Client", style="cyan", width=18)
        table_display.add_column("Contact support", style="green")
        table_display.add_column("Début", style="magenta", width=10)
        table_display.add_column("Fin", style="magenta", width=10)
        table_display.add_column("Lieu", style="green")
        table_display.add_column("Nombre de personnes", style="cyan")
        table_display.add_column("Notes", style="magenta", no_wrap=True)

        if all:
            for row in result:
                if row.support_contact_id is not None:
                    support_contact = f"{row.support_contact.first_name} {row.support_contact.name}"
                else:
                    support_contact = None
                table_display.add_row(
                    f"{row.id}",
                    f"{row.name}",
                    f"{row.contract_id}",
                    f"{row.client.fullname} {row.client.email} tel:{row.client.phone}",
                    support_contact,
                    f"{row.event_date_start}",
                    f"{row.event_date_end}",
                    f"{row.location}",
                    f"{row.attendees}",
                    f"{row.notes}",
                )

            return table_display
        else:
            if result.support_contact_id is not None:
                support_contact = f"{result.support_contact.first_name} {result.support_contact.name}"
            else:
                support_contact = None
            table_display.add_row(
                f"{result.id}",
                f"{result.name}",
                f"{result.contract_id}",
                f"{result.client.fullname} {result.client.email} tel:{result.client.phone}",
                support_contact,
                f"{result.event_date_start}",
                f"{result.event_date_end}",
                f"{result.location}",
                f"{result.attendees}",
                f"{result.notes}",
            )
            return table_display

    def table_staff(self, result, all):
        """
        Construct the staff table for display.

        Args:
            result: The result of the staff query.
            all (bool): Indicates if there are multiple rows (True) or one row (False).

        Returns:
            Table: The constructed staff table.
        """
        table_display = Table(
            title="Collaborateurs",
            show_lines=True,
            box=box.MINIMAL_DOUBLE_HEAD,
            expand=True,
        )
        table_display.add_column("Id", style="cyan", no_wrap=True)
        table_display.add_column("Nom", style="magenta", no_wrap=True)
        table_display.add_column("Prénom", style="magenta", no_wrap=True)
        table_display.add_column("Email", style="green", no_wrap=True)
        table_display.add_column("Mot de passe", style="cyan", width=8)
        table_display.add_column("Département", style="magenta", no_wrap=True)

        if all:
            for row in result:
                table_display.add_row(
                    f"{row.id}",
                    f"{row.name}",
                    f"{row.first_name}",
                    f"{row.email}",
                    f"{row.password}",
                    f"{row.department.name}",
                )

            return table_display
        else:
            table_display.add_row(
                f"{result.id}",
                f"{result.name}",
                f"{result.first_name}",
                f"{result.email}",
                f"{result.password}",
                f"{result.department.name}",
            )
            return table_display

    def clean(self):
        """Clear the console display"""
        if platform.system() == "Windows":
            os.system("cls")
        elif platform.system() == "Linux":
            os.system("clear")
